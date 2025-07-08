from .data_loader import load_annotations

def train():
    data = load_annotations()
    print("داده‌های آنوتیشن شده:")
    for item in data:
        print(item)

if __name__ == "__main__":
    train()
