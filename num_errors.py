from keras.applications import DenseNet201
model = DenseNet201(weights = "imagenet", include_top=False, input_shape = (img_rows, img_cols, 3))

from keras.layers import Flatten, Dense, Dropout, BatchNormalization
from keras.regularizers import l2
#Adding custom Layers 
x = model.output
x = Flatten()(x)
x = Dense(2048, activation="elu", kernel_regularizer=l2(0.0001), bias_regularizer=l2(0.0001))(x)
x = BatchNormalization()(x)
# x = Dropout(0.5)(x)
x = Dense(1024, activation="elu", kernel_regularizer=l2(0.0001), bias_regularizer=l2(0.0001))(x)
x = BatchNormalization()(x)
# x = Dropout(0.5)(x)
predictions = Dense(1, activation="sigmoid", kernel_regularizer=l2(0.0001), bias_regularizer=l2(0.0001))(x)

from keras.models import Model
# creating the final model 
model_final = Model(input = model.input, output = predictions)







###########################################################################################################################
print("OS: ", sys.platform)
print("Python: ", sys.version)
print("Keras: ", K.__version__)
print("Numpy: ", np.__version__)
print("Tensorflow: ", tensorflow.__version__)
print(K.backend.backend())
print(K.backend.image_data_format())
print("GPU: ", get_gpu_name())
print(get_cuda_version())
print("CuDNN Version ", get_cudnn_version())


CPU_COUNT = multiprocessing.cpu_count()
GPU_COUNT = len(get_gpu_name())
print("CPUs: ", CPU_COUNT)
print("GPUs: ", GPU_COUNT)
##########################################################################################################################
# Create a generator for prediction
validation_generator = validation_datagen.flow_from_directory(
        validation_dir,
        target_size=(image_size, image_size),
        batch_size=1,
        class_mode='categorical',
        shuffle=False)

# Get the filenames from the generator
fnames = validation_generator.filenames

# Get the ground truth from generator
ground_truth = validation_generator.classes

# Get the label to class mapping from the generator
label2index = validation_generator.class_indices

# Getting the mapping from class index to class label
idx2label = dict((v,k) for k,v in label2index.items())

# Get the predictions from the model using the generator
predictions = model.predict_generator(validation_generator, steps=validation_generator.samples/validation_generator.batch_size,verbose=1)
predicted_classes = np.argmax(predictions,axis=1)
#print (predictions)

errors = np.where(predicted_classes != ground_truth)[0]
print("No of errors = {}/{}".format(len(errors),validation_generator.samples))

# Show the errors
for i in range(len(errors)):
    pred_class = np.argmax(predictions[errors[i]])
    pred_label = idx2label[pred_class]
    
    title = 'Original label:{}, Prediction :{}, confidence : {:.3f}, class ID : {}'.format(
        fnames[errors[i]].split('/')[0],
        pred_label,
        predictions[errors[i]][pred_class], pred_class)
    
    original = load_img('{}/{}'.format(validation_dir,fnames[errors[i]]))
    plt.figure(figsize=[7,7])
    plt.axis('off')
    plt.title(title)
    plt.imshow(original)
    plt.show()
#################################################################################################################
fnames = validation_generator2.filenames
 
ground_truth = validation_generator2.classes
 
label2index = validation_generator2.class_indices
 
# Getting the mapping from class index to class label
idx2label = dict((v,k) for k,v in label2index.items())
prob = model.predict_generator(validation_generator2)
predictions=np.argmax(prob,axis=1)

errors = np.where(predictions != ground_truth)[0]
print("No of errors = {}/{}".format(len(errors),nb_validation_samples))
####################################################################################################################
testing_generator = validation_datagen.flow_from_directory(
        test_dir,
        target_size=(height, width),
        batch_size=val_batchsize,
        class_mode='categorical',
        shuffle=False)
 
# Get the filenames from the generator
fnames = testing_generator.filenames
 
# Get the ground truth from generator
ground_truth = testing_generator.classes
 
# Get the label to class mapping from the generator
label2index = testing_generator.class_indices
 
# Getting the mapping from class index to class label
idx2label = dict((v,k) for k,v in label2index.items())
 
# Get the predictions from the model using the generator
predictions = model.predict_generator(testing_generator, 
                                      steps=testing_generator.samples/testing_generator.batch_size,
                                      verbose=1)
predicted_classes = np.argmax(predictions,axis=1)
 
errors = np.where(predicted_classes != ground_truth)[0]
print("No of errors = {}/{}".format(len(errors),testing_generator.samples))
print(str(len(errors)/testing_generator.samples) + "%")
####################################################################################################################

probabilities = model.predict_generator(test_generator, 600)
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import numpy as np
y_true = np.array([0] * 100 + [1] * 100 + [2] * 100 + [3] * 100 + [4] *100 + [5] *100 )
#y_pred = probabilities > 0.5
print(probabilities)
y_pred = np.asarray(probabilities)
y_pred = np.argmax(probabilities,axis=1)

print(y_pred)

print(y_true)

#print(np.shape(probabilities))
print(confusion_matrix(y_true, y_pred))

print(accuracy_score(y_true, y_pred))

####################################################################################################################
from tensorflow.python.client import device_lib
device_lib.list_local_devices()
####################################################################################################################
test_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    color_mode='landsat',
    batch_size=5000,
    class_mode='binary')

X_test = test_generator.next()

y_pred = model.predict(X_test[0])
y_true = X_test[1]
roc_auc_score(y_true, y_pred)


####################################################################################################################
predictions = np.round(model_mura.predict_generator(test_generator, steps=3197//1))
predictions = predictions.flatten()
y_true = test_generator.classes

def print_all_metrics(y_true, y_pred):
    print("roc_auc_score: ", roc_auc_score(y_true, y_pred))
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

    print("Sensitivity: ", get_sensitivity(tp, fn))
    print("Specificity: ", get_specificity(tn, fp))
    print("Cohen-Cappa-Score: ", cohen_kappa_score(y_true, y_pred))
    print("F1 Score: ", f1_score(y_true, y_pred))


def get_sensitivity(tp, fn):
    return tp / (tp + fn)


def get_specificity(tn, fp):
return tn / (tn + fp)


print_all_metrics(y_true,y_pred)

####################################################################################################################
####################################################################################################################
####################################################################################################################
model.fit(x_train, y_train, nb_epoch=5, batch_size=64, class_weight=myclass_weight)

	#Evaluate the scores of the model
	scores = model.evaluate(x_test, y_test, verbose=0)
	print("Accuracy: %.2f%%" % (scores[1]*100))
	probas = model.predict(x_test)
	pred_indices = np.argmax(probas, axis=1)
	classes = np.array(range(0,9))
	preds = classes[pred_indices]
	#model.save('../models/cnn_model4.h5')
	print('Log loss: {}'.format(log_loss(classes[np.argmax(y_test, axis=1)], probas)))
print('Accuracy: {}'.format(accuracy_score(classes[np.argmax(y_test, axis=1)], preds))) 





####################################################################################################################

class_test=model_emotion.predict_classes(X_test)


classes = np.array(range(0,7))
classes
accuracy_score(classes[np.argmax(Y_test, axis=1)], class_test)


####################################################################################################################

model.fit_generator(datagen.flow(x_train, y_train,
                        batch_size=batch_size),
                        epochs=epochs,
                        workers=4)

y_pred = np.argmax(model.predict(x_test), axis=-1)
print(precision_score(y_test, y_pred, average='macro'))
print(recall_score(y_test, y_pred, average='macro'))
print(accuracy_score(y_test, y_pred))
print(f1_score(y_test, y_pred, average='macro'))

####################################################################################################################

import keras.backend as K

def f1_score(y_true, y_pred):

    # Count positive samples.
    c1 = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    c2 = K.sum(K.round(K.clip(y_pred, 0, 1)))
    c3 = K.sum(K.round(K.clip(y_true, 0, 1)))

    # If there are no true samples, fix the F1 score at 0.
    if c3 == 0:
        return 0

    # How many selected items are relevant?
    precision = c1 / c2

    # How many relevant items are selected?
    recall = c1 / c3

    # Calculate f1_score
    f1_score = 2 * (precision * recall) / (precision + recall)
    return f1_score

def recall_score(y_true, y_pred):

    # Count positive samples.
    c1 = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    c2 = K.sum(K.round(K.clip(y_pred, 0, 1)))
    c3 = K.sum(K.round(K.clip(y_true, 0, 1)))

    # If there are no true samples, fix the F1 score at 0.
    if c3 == 0:
        return 0

    # How many relevant items are selected?
    recall_score = c1 / c3

    return recall_score


# Train the model

# compile the model
model.compile(loss='categorical_crossentropy',
             optimizer=optimizers.RMSprop(lr=1e-4,decay=0.9),
             metrics=['accuracy',f1_score,recall_score])

# Train the model
history = model.fit_generator(
      train_generator,
      steps_per_epoch=train_generator.samples/train_generator.batch_size ,
      epochs=30,
      validation_data=validation_generator,
      validation_steps=validation_generator.samples/validation_generator.batch_size, verbose=1)

####################################################################################################################


import numpy as np
from tqdm import tqdm
train_set.reset()
n_steps = train_set.n // train_set.batch_size
y_preds = []
y_true = []
for i in tqdm(range(n_steps)):
    x_batch, y_batch = test_set.next()
    preds = classifier.predict(x_batch)
    y_preds.extend([np.argmax(pred) for pred in preds])
    y_true.extend([np.argmax(y) for y in y_batch])

from sklearn.metrics import f1_score
f1 = f1_score(y_true, y_preds, average='macro')
print('F1: {:.3f}'.format(f1))




####################################################################################################################
model.fit(X_train, Y_train, validation_data=(X_valid,Y_valid),batch_size=32, \
              epochs=10, verbose=1)
score = model.evaluate(X_test, Y_test)
result = model.predict(X_test)
f1_score(Y_test, result, average='weighted')

####################################################################################################################

filenames = test_generator.filenames
nb_samples = len(filenames)
predict = classifier.predict_generator(test_generator,steps = nb_samples)

pred_prob = np.argmax(predict, axis=-1) #multiple categories

label_map = (training_set.class_indices)
label_map = dict((v,k) for k,v in label_map.items()) #flip k,v
predictions = [label_map[k] for k in pred_prob]

correct, wrong = 0,0
for ypred, ytrue in zip(predictions,test_generator.filenames):
    if ypred== re.findall('[a-z]{1,2}', ytrue.split('_')[1])[0]:
	correct +=1
    else:
	 wrong +=

accuracy = float(correct)/float(len(test_generator.filenames))
print(accuracy)

####################################################################################################################
##### Learn

history = model.fit_generator(datagen.flow(train_X, train_y, batch_size=128),
epochs=100, validation_data=(valid_X, valid_y), workers=4)

pred_y = model.predict(test_X)
pred_y = np.argmax(pred_y, 1)
####################################################################################################################
from sklearn.metrics import precision_score, recall_score, accuracy_score, f1_score

model.fit_generator(datagen.flow(x_train, y_train,
                        batch_size=batch_size),
                        epochs=epochs,
                        workers=4)

y_pred = np.argmax(model.predict(x_test), axis=-1)
print(precision_score(y_test, y_pred, average='macro'))
print(recall_score(y_test, y_pred, average='macro'))
print(accuracy_score(y_test, y_pred))
print(f1_score(y_test, y_pred, average='macro'))



####################################################################################################################
from sklearn.metrics import precision_score, recall_score, accuracy_score, f1_score
model.fit_generator(datagen.flow(x_train, y_train,
                        batch_size=batch_size),
                        epochs=epochs,
                        workers=4)

y_pred = np.argmax(model.predict(x_test), axis=-1)
print(precision_score(y_test, y_pred, average='macro'))
print(recall_score(y_test, y_pred, average='macro'))
print(accuracy_score(y_test, y_pred))
print(f1_score(y_test, y_pred, average='macro'))


####################################################################################################################



####################################################################################################################




####################################################################################################################



####################################################################################################################



####################################################################################################################





####################################################################################################################



####################################################################################################################



####################################################################################################################





####################################################################################################################



####################################################################################################################



####################################################################################################################





####################################################################################################################



####################################################################################################################



####################################################################################################################








####################################################################################################################




####################################################################################################################



####################################################################################################################



####################################################################################################################




####################################################################################################################



####################################################################################################################



####################################################################################################################





####################################################################################################################



####################################################################################################################



####################################################################################################################





####################################################################################################################



####################################################################################################################



####################################################################################################################





####################################################################################################################



####################################################################################################################



####################################################################################################################








####################################################################################################################




####################################################################################################################



####################################################################################################################



####################################################################################################################




####################################################################################################################



####################################################################################################################



####################################################################################################################





####################################################################################################################



####################################################################################################################



####################################################################################################################





####################################################################################################################



####################################################################################################################



####################################################################################################################





####################################################################################################################



####################################################################################################################



####################################################################################################################






