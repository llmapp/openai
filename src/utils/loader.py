from transformers import AutoTokenizer, AutoModel

model = None
tokenizer = None


def load_model(model_id: str):
    global model, tokenizer

    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    model = AutoModel.from_pretrained(model_id, trust_remote_code=True).cuda()
    model.eval()


def get_model():
    global model, tokenizer
    return model, tokenizer
