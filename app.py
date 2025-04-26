from src.pipeline.training_pipeline import TrainingPipeline

if __name__ == "__main__":
    training_pipeline = TrainingPipeline()
    training_pipeline.start_model_evaluation()