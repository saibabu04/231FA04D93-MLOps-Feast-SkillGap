from datetime import timedelta
from feast import Entity, FeatureView, FeatureService, Field, FileSource
from feast.types import Float32, Int64, String

skill = Entity(name="skill", join_keys=["skill_id"], description="Unique CSE graduate skill-gap entity")

skillgap_source = FileSource(
    name="cse_skillgap_source",
    path="data/cse_skillgap_features.parquet",
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp",
)

skillgap_feature_view = FeatureView(
    name="cse_skillgap_features",
    entities=[skill],
    ttl=timedelta(days=3650),
    schema=[
        Field(name="curriculum_score", dtype=Float32),
        Field(name="industry_score", dtype=Float32),
        Field(name="practical_score", dtype=Float32),
        Field(name="projects_completed", dtype=Int64),
        Field(name="internships_completed", dtype=Int64),
        Field(name="certifications", dtype=Int64),
        Field(name="coding_score", dtype=Float32),
        Field(name="communication_score", dtype=Float32),
        Field(name="problem_solving_score", dtype=Float32),
        Field(name="teamwork_score", dtype=Float32),
        Field(name="industry_demand_score", dtype=Float32),
        Field(name="curriculum_relevance_score", dtype=Float32),
        Field(name="skill_gap", dtype=Float32),
        Field(name="employability_score", dtype=Float32),
        Field(name="gap_level", dtype=String),
    ],
    source=skillgap_source,
    online=True,
)

cse_skillgap_service = FeatureService(
    name="cse_skillgap_prediction_service",
    features=[skillgap_feature_view],
)
