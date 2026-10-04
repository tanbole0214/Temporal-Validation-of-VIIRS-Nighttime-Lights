"""Unchanged statistical function bodies from the frozen R4/R5 estimator."""
import numpy as np
import pandas as pd
PRODUCTS = {'EOG': 'eog_dln_light_extended', 'Black Marble': 'bm_dln_light_extended'}
BENCHMARKS = ('B0','B1','B2','B3')
STANDALONE_YEARS = tuple(range(2015,2025))
CONDITIONAL_YEARS = tuple(range(2016,2025))
def domain_for(year, conditional=False):
    return 'primary_high_coverage' if year<=2019 else 'near_national_stress' if year<=2021 else 'post2021_extension'

def score(y: np.ndarray, pred: np.ndarray) -> dict[str, float]:
    y = np.asarray(y, float)
    pred = np.asarray(pred, float)
    error = y - pred
    sse = float(error @ error)
    mse = float(np.mean(error**2))
    sst = float(np.sum((y - y.mean()) ** 2))
    return {
        "N": len(y),
        "RMSE": float(np.sqrt(mse)),
        "MAE": float(np.mean(np.abs(error))),
        # Match the frozen computation (and all regional residual summaries).
        # The old SI note labelled the opposite sign; that label is corrected,
        # not the historical numeric values or any loss/skill estimand.
        "mean_error": float(error.mean()),
        "SSE": sse,
        "OOS_R2_test_mean": float(1 - sse / sst) if sst > 0 else np.nan,
    }


def fit_ols(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    design = np.column_stack([np.ones(len(y)), x])
    return np.linalg.lstsq(design, y, rcond=None)[0]


def benchmark_predictions(
    panel: pd.DataFrame,
    rows: pd.DataFrame,
    prediction_year: int,
    light_var: str,
) -> pd.DataFrame:
    history = panel.loc[
        panel["year"].lt(prediction_year),
        ["city_code", "province_code", "year", "transformed_log_growth_extended", light_var],
    ].dropna(subset=["transformed_log_growth_extended", light_var])
    if history.empty:
        raise RuntimeError(f"No admissible history before {prediction_year}")
    output = rows[["city_code", "province_code"]].copy().reset_index(drop=True)
    national = float(history["transformed_log_growth_extended"].mean())
    national_max = int(history["year"].max())
    output["predicted_B0"] = national
    output["source_B0"] = "national_training_mean"
    output["max_gdp_year_used_B0"] = national_max

    province_mean = history.groupby("province_code")["transformed_log_growth_extended"].mean()
    province_max = history.groupby("province_code")["year"].max()
    output["predicted_B1"] = output["province_code"].map(province_mean)
    output["max_gdp_year_used_B1"] = output["province_code"].map(province_max)
    missing = output["predicted_B1"].isna()
    output["source_B1"] = np.where(missing, "fallback_B0", "province_training_mean")
    output.loc[missing, "predicted_B1"] = national
    output.loc[missing, "max_gdp_year_used_B1"] = national_max

    city_mean = history.groupby("city_code")["transformed_log_growth_extended"].mean()
    city_max = history.groupby("city_code")["year"].max()
    output["predicted_B2"] = output["city_code"].map(city_mean)
    output["max_gdp_year_used_B2"] = output["city_code"].map(city_max)
    missing = output["predicted_B2"].isna()
    output["source_B2"] = np.where(missing, "fallback_B1", "prefecture_training_mean")
    output.loc[missing, "predicted_B2"] = output.loc[missing, "predicted_B1"]
    output.loc[missing, "max_gdp_year_used_B2"] = output.loc[missing, "max_gdp_year_used_B1"]

    recent = history.sort_values(["city_code", "year"]).groupby("city_code").tail(1).set_index("city_code")
    output["predicted_B3"] = output["city_code"].map(recent["transformed_log_growth_extended"])
    output["max_gdp_year_used_B3"] = output["city_code"].map(recent["year"])
    missing = output["predicted_B3"].isna()
    output["source_B3"] = np.where(missing, "fallback_B2", "last_observed_prefecture_growth")
    output.loc[missing, "predicted_B3"] = output.loc[missing, "predicted_B2"]
    output.loc[missing, "max_gdp_year_used_B3"] = output.loc[missing, "max_gdp_year_used_B2"]
    return output


def run_standalone(panel: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    prediction_frames = []
    metric_rows = []
    for target_year in STANDALONE_YEARS:
        for product, light_var in PRODUCTS.items():
            train = panel.loc[panel["year"].lt(target_year)].dropna(
                subset=["transformed_log_growth_extended", light_var]
            )
            target = panel.loc[panel["year"].eq(target_year)].dropna(
                subset=["transformed_log_growth_extended", light_var]
            ).reset_index(drop=True)
            if train.empty or target.empty:
                raise RuntimeError(f"Empty stand-alone fold: {product} {target_year}")
            beta = fit_ols(
                train[light_var].to_numpy(),
                train["transformed_log_growth_extended"].to_numpy(),
            )
            benchmarks = benchmark_predictions(panel, target, target_year, light_var)
            pred = target[
                [
                    "city_code", "city_name", "province_code", "province_name", "macro_region",
                    "centroid_lon", "centroid_lat", "year", "transformed_log_growth_extended", light_var,
                ]
            ].copy()
            pred = pred.rename(
                columns={
                    "year": "target_year",
                    "transformed_log_growth_extended": "actual_gdp_growth",
                    light_var: "target_year_light_change",
                }
            )
            pred.insert(0, "product", product)
            pred.insert(1, "temporal_domain", domain_for(target_year))
            pred["training_years"] = "|".join(map(str, sorted(train["year"].unique())))
            pred["max_training_year"] = int(train["year"].max())
            pred["light_intercept"] = float(beta[0])
            pred["light_slope"] = float(beta[1])
            pred["predicted_light_mapping"] = beta[0] + beta[1] * pred["target_year_light_change"]
            for column in benchmarks.columns:
                if column not in ("city_code", "province_code"):
                    pred[column] = benchmarks[column].to_numpy()
            pred["target_year_GDP_used_in_fit"] = False
            prediction_frames.append(pred)

            light_score = score(pred["actual_gdp_growth"], pred["predicted_light_mapping"])
            for benchmark in BENCHMARKS:
                benchmark_score = score(pred["actual_gdp_growth"], pred[f"predicted_{benchmark}"])
                delta = (
                    (pred["actual_gdp_growth"] - pred["predicted_light_mapping"]) ** 2
                    - (pred["actual_gdp_growth"] - pred[f"predicted_{benchmark}"]) ** 2
                )
                metric_rows.append(
                    {
                        "product": product,
                        "temporal_domain": domain_for(target_year),
                        "target_year": target_year,
                        "training_years": pred["training_years"].iloc[0],
                        "max_training_year": int(pred["max_training_year"].iloc[0]),
                        "benchmark": benchmark,
                        "N": len(pred),
                        "N_provinces": pred["province_code"].nunique(),
                        "light_intercept": float(beta[0]),
                        "light_slope": float(beta[1]),
                        **{f"light_{key}": value for key, value in light_score.items()},
                        **{f"benchmark_{key}": value for key, value in benchmark_score.items()},
                        "skill_vs_benchmark": float(1 - light_score["SSE"] / benchmark_score["SSE"]),
                        "mean_delta_loss": float(delta.mean()),
                        "median_delta_loss": float(delta.median()),
                        "benchmark_fallback_n": int(pred[f"source_{benchmark}"].str.startswith("fallback").sum()),
                    }
                )
    predictions = pd.concat(prediction_frames, ignore_index=True)
    return predictions, pd.DataFrame(metric_rows)


def build_nested_data(
    panel: pd.DataFrame, product: str, light_var: str, target_year: int
) -> tuple[pd.DataFrame, pd.DataFrame, list[dict]]:
    training_parts = []
    leakage_rows = []
    for residual_year in range(2015, target_year):
        current = panel.loc[panel["year"].eq(residual_year)].dropna(
            subset=["transformed_log_growth_extended", light_var]
        ).reset_index(drop=True)
        if current.empty:
            continue
        bench = benchmark_predictions(panel, current, residual_year, light_var)
        part = current[
            [
                "city_code", "city_name", "province_code", "province_name", "macro_region",
                "year", "transformed_log_growth_extended", light_var, "centroid_lon", "centroid_lat",
            ]
        ].copy()
        part = part.rename(
            columns={
                "year": "prediction_year",
                "transformed_log_growth_extended": "y",
                light_var: "x",
            }
        )
        for column in bench.columns:
            if column not in ("city_code", "province_code"):
                part[column] = bench[column].to_numpy()
        training_parts.append(part)
        for benchmark in BENCHMARKS:
            violations = int((part[f"max_gdp_year_used_{benchmark}"] >= residual_year).sum())
            leakage_rows.append(
                {
                    "product": product,
                    "target_year": target_year,
                    "row_role": "training_residual",
                    "prediction_year": residual_year,
                    "benchmark": benchmark,
                    "N": len(part),
                    "max_gdp_year_used": part[f"max_gdp_year_used_{benchmark}"].max(),
                    "violations": violations,
                }
            )
    train = pd.concat(training_parts, ignore_index=True)
    target = panel.loc[panel["year"].eq(target_year)].dropna(
        subset=["transformed_log_growth_extended", light_var]
    ).reset_index(drop=True)
    bench = benchmark_predictions(panel, target, target_year, light_var)
    target_out = target[
        [
            "city_code", "city_name", "province_code", "province_name", "macro_region", "year",
            "transformed_log_growth_extended", light_var, "centroid_lon", "centroid_lat",
        ]
    ].copy()
    target_out = target_out.rename(
        columns={"year": "prediction_year", "transformed_log_growth_extended": "y", light_var: "x"}
    )
    for column in bench.columns:
        if column not in ("city_code", "province_code"):
            target_out[column] = bench[column].to_numpy()
    for benchmark in BENCHMARKS:
        violations = int((target_out[f"max_gdp_year_used_{benchmark}"] >= target_year).sum())
        leakage_rows.append(
            {
                "product": product,
                "target_year": target_year,
                "row_role": "target_prediction",
                "prediction_year": target_year,
                "benchmark": benchmark,
                "N": len(target_out),
                "max_gdp_year_used": target_out[f"max_gdp_year_used_{benchmark}"].max(),
                "violations": violations,
            }
        )
    return train, target_out, leakage_rows


def run_conditional(panel: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    metric_rows = []
    prediction_frames = []
    leakage_rows = []
    for target_year in CONDITIONAL_YEARS:
        for product, light_var in PRODUCTS.items():
            train, target, audit = build_nested_data(panel, product, light_var, target_year)
            leakage_rows.extend(audit)
            for benchmark in BENCHMARKS:
                q_train = train["y"].to_numpy(float) - train[f"predicted_{benchmark}"].to_numpy(float)
                beta = fit_ols(train["x"].to_numpy(float), q_train)
                alpha0 = float(q_train.mean())
                raw_prediction = target[f"predicted_{benchmark}"].to_numpy(float)
                pred_m0 = raw_prediction + alpha0
                pred_m1 = raw_prediction + beta[0] + beta[1] * target["x"].to_numpy(float)
                y = target["y"].to_numpy(float)
                m0 = score(y, pred_m0)
                m1 = score(y, pred_m1)
                raw = score(y, raw_prediction)
                delta = (y - pred_m1) ** 2 - (y - pred_m0) ** 2
                metric_rows.append(
                    {
                        "product": product,
                        "temporal_domain": domain_for(target_year, conditional=True),
                        "benchmark": benchmark,
                        "target_year": target_year,
                        "N_target": len(target),
                        "N_provinces": target["province_code"].nunique(),
                        "N_training": len(train),
                        "N_training_years": train["prediction_year"].nunique(),
                        "training_years": "|".join(map(str, sorted(train["prediction_year"].unique()))),
                        "alpha_M0": alpha0,
                        "alpha_M1": float(beta[0]),
                        "gamma_M1": float(beta[1]),
                        **{f"M0_{key}": value for key, value in m0.items()},
                        **{f"M1_{key}": value for key, value in m1.items()},
                        **{f"raw_benchmark_{key}": value for key, value in raw.items()},
                        "IncSkill_M1_vs_M0": float(1 - m1["SSE"] / m0["SSE"]),
                        "PracticalSkill_M1_vs_raw_benchmark": float(1 - m1["SSE"] / raw["SSE"]),
                        "mean_delta_loss": float(delta.mean()),
                        "median_delta_loss": float(np.median(delta)),
                    }
                )
                pred = target[
                    [
                        "city_code", "city_name", "province_code", "province_name", "macro_region",
                        "centroid_lon", "centroid_lat", "prediction_year", "y", "x",
                    ]
                ].copy()
                pred.insert(0, "product", product)
                pred.insert(1, "temporal_domain", domain_for(target_year, conditional=True))
                pred["benchmark"] = benchmark
                pred["predicted_raw_benchmark"] = raw_prediction
                pred["predicted_M0"] = pred_m0
                pred["predicted_M1"] = pred_m1
                pred["error_M0"] = y - pred_m0
                pred["error_M1"] = y - pred_m1
                pred["delta_loss"] = delta
                pred["alpha_M0"] = alpha0
                pred["alpha_M1"] = float(beta[0])
                pred["gamma_M1"] = float(beta[1])
                prediction_frames.append(pred)
    return (
        pd.concat(prediction_frames, ignore_index=True),
        pd.DataFrame(metric_rows),
        pd.DataFrame(leakage_rows),
    )
