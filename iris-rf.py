import mlflow
import mlflow.sklearn 
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import dagshub
dagshub.init(repo_owner='Pacesetter55', repo_name='mlflow-dagshub-demo', mlflow=True)

iris= load_iris()
X=iris.data
y=iris.target

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

max_depth=50
n_estimators=50
mlflow.set_tracking_uri("https://dagshub.com/Pacesetter55/mlflow-dagshub-demo.mlflow")
mlflow.set_experiment('iris-rf')
with mlflow.start_run():
    rf=RandomForestClassifier(max_depth=max_depth,n_estimators=n_estimators)
    rf.fit(X_train,y_train)
    preds=rf.predict(X_test)
    mlflow.log_metric('accuracy',accuracy_score(y_test,preds))
    mlflow.log_param('max_depth',max_depth)
    mlflow.log_param('n_estimators',n_estimators)
    mlflow.log_artifact(__file__)
    mlflow.sklearn.log_model(rf,"Random Forest")
    cm=confusion_matrix(y_test,preds)
    plt.figure(figsize=(6,6))
    sns.heatmap(cm,annot=True,fmt='d',cmap='Blues',xticklabels=iris.target_names,yticklabels=iris.target_names)
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.title('Confusion Matrix')
    plt.savefig('confusion_matrix.png')
    #mlflow code
    mlflow.set_tag("author",'rahul')
    mlflow.set_tag("model",'random-forest')
    mlflow.log_artifact("confusion_matrix.png")
    print('accuracy',accuracy_score(y_test,preds))