
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Config, AdamW
import pandas as pd

class EconomicNewsDataset(Dataset): # ToDo：データセットを準備する（txtファイル = ニュースの本文,感情数値（0-100））,感情の数値化方法を検討
    def __init__(self, tokenizer, file_path, max_length):
        self.tokenizer = tokenizer
        self.data = pd.read_csv(file_path)
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        article = str(self.data.iloc[index]['article'])
        sentiment_score = float(self.data.iloc[index]['sentiment_score'])
        encoding = self.tokenizer.encode_plus(
            article,
            add_special_tokens=True,
            max_length=self.max_length,
            return_token_type_ids=False,
            padding='max_length',
            return_attention_mask=True,
            return_tensors='pt',
        )

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(sentiment_score, dtype=torch.float)
        }

def initialize_model(tokenizer, train_data_loader):
    config = GPT2Config.from_pretrained('gpt2', output_hidden_states=False)
    model = GPT2LMHeadModel.from_pretrained('gpt2', config=config)

    # カスタム層を追加して感情スコアを予測
    model.sentiment_score = torch.nn.Linear(config.n_embd, 1)

    return model

def train(epoch, model, data_loader, optimizer):
    model.train()
    total_loss = 0

    for batch in data_loader:
        inputs = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)

        optimizer.zero_grad()

        outputs = model(inputs, attention_mask=attention_mask)
        logits = model.sentiment_score(outputs.logits)

        loss = torch.nn.functional.mse_loss(logits, labels)
        total_loss += loss.item()

        loss.backward()
        optimizer.step()

    average_loss = total_loss / len(data_loader)
    print(f"Epoch {epoch} Average Loss: {average_loss}")

# ハイパーパラメータの設定
BATCH_SIZE = 8
MAX_LEN = 512
EPOCHS = 4

# トークナイザの初期化
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# データセットとデータローダーの準備
train_dataset = EconomicNewsDataset(tokenizer, 'path_to_your_train_data.csv', max_length=MAX_LEN)
train_data_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE)

# モデルの初期化
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = initialize_model(tokenizer, train_data_loader).to(device)

# オプティマイザーの設定
optimizer = AdamW(model.parameters(), lr=5e-5)

# トレーニング
for epoch in range(EPOCHS):
    train(epoch, model, train_data_loader, optimizer)


#chatGPT出力
#注意点
#このコードは基本的な構造を提供しますが、実際にはデータセットのパス、ハイパーパラメータ、カスタム層の設計など、プロジェクトの要件に合わせて調整が必要です。
#データセットのサイズやモデルの複雑さに応じて、GPUを使用することをお勧めします。
#このコードは簡略化された例です。実際のプロジェクトでは、バリデーションステップ、保存とロードの機能、適切なエラーハンドリング、ロギングなどを追加する必要があります。