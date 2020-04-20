from tensorflow.keras import backend as K
#metric creation for Keras
def prec_m(y_true, y_pred):
    tp = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    pp = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = tp / (pp + K.epsilon())
    return precision

def recall_m(y_true, y_pred):
    tp = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    pp = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = tp / (pp + K.epsilon())
    return recall

def f1_m(y_true, y_pred):
    precision = prec_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision + recall + K.epsilon()))

def rmse(y_true, y_pred):
    return K.sqrt(K.mean(K.square(y_pred - y_true), axis=-1))