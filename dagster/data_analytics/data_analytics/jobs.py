from dagster import define_asset_job, AssetSelection

indebted_data_analytics_job = define_asset_job(name="indebted_data_analytics_job", selection=AssetSelection.all())
