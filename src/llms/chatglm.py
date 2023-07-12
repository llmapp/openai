from transformers import AutoTokenizer, AutoModel


def load_model(model_id: str):
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    model = AutoModel.from_pretrained(model_id, trust_remote_code=True).cuda()
    model.eval()

    return model, tokenizer
