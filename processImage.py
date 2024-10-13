import torch
import clip
import pandas
from PIL import Image
from check_item import check_item_in_csv, check_item_in_dataframe


class ImageProcessor:
    compostdata = pandas.read_csv('./compost_data/compost_data.csv', header=None)
    nameList = compostdata[0].values.tolist()
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)

    def process(self, path):
        image = self.preprocess(Image.open(path)).unsqueeze(0).to(self.device)
        text = clip.tokenize(self.nameList).to(self.device)

        with torch.no_grad():
            image_features = self.model.encode_image(image)
            text_features = self.model.encode_text(text)

            logits_per_image, logits_per_text = self.model(image, text)
            probs = logits_per_image.softmax(dim=-1).cpu().numpy()

        name= self.nameList[probs.argmax()]
        value = check_item_in_dataframe(name, self.compostdata)
        return name,value