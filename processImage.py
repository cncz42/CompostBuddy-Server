import torch
import clip
from PIL import Image


class ImageProcessor:
    tokenlist = ["a diagram", "a flow chart", "a dog", "a cat", "a fruit", "a banana", "a png"]
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)

    def process(self, path):
        image = self.preprocess(Image.open(path)).unsqueeze(0).to(self.device)
        text = clip.tokenize(self.tokenlist).to(self.device)

        with torch.no_grad():
            image_features = self.model.encode_image(image)
            text_features = self.model.encode_text(text)

            logits_per_image, logits_per_text = self.model(image, text)
            probs = logits_per_image.softmax(dim=-1).cpu().numpy()

        return self.tokenlist[probs.argmax()]