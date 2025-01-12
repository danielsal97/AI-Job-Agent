import torch


def cosine_similarity(embedding1, embedding2):
    """Calculate similarity using PyTorch's cosine similarity."""
    return torch.nn.functional.cosine_similarity(embedding1.unsqueeze(0), embedding2.unsqueeze(0)).item()


def dot_product_similarity(embedding1, embedding2):
    """Calculate similarity using dot product."""
    embedding1 = embedding1 / torch.norm(embedding1)
    embedding2 = embedding2 / torch.norm(embedding2)
    return torch.dot(embedding1, embedding2).item()


def calculate_scores(resume_embedding, job_embedding, method="dot_product"):
    """Calculate similarity scores using the specified metric."""
    if method == "cosine":
        job_matches_cv = cosine_similarity(resume_embedding, job_embedding)
        cv_matches_job = cosine_similarity(job_embedding, resume_embedding)
    elif method == "dot_product":
        job_matches_cv = dot_product_similarity(resume_embedding, job_embedding)
        cv_matches_job = dot_product_similarity(job_embedding, resume_embedding)
    else:
        raise ValueError("Unsupported similarity method")

    semantic_match = (job_matches_cv + cv_matches_job) / 2
    contextual_match = job_matches_cv * 0.8  # Weighted score
    overall_score = (job_matches_cv + cv_matches_job + semantic_match + contextual_match) / 4

    return {
        "job_matches_cv": job_matches_cv,
        "cv_matches_job": cv_matches_job,
        "semantic_match": semantic_match,
        "contextual_match": contextual_match,
        "overall_score": overall_score,
    }