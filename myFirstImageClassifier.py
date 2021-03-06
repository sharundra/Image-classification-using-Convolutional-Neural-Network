import tensorflow as tf
from NetworkBuilder  import NetworkBuilder
from DatasetGenerator import DataSetGenerator, seperateData
import datetime
import numpy as np
import os

with tf.name_scope("Input_layer") as scope:
    Input = tf.placeholder(dtype = "float", shape = [None, 128, 128, 1], name = "Input")

with tf.name_scope("Target_layer") as scope:
    Target = tf.placeholder(dtype = "float", shape = [None, 2], name = "Target")

nb = NetworkBuilder()

with tf.name_scope("MyAwesomeModel") as scope:
    model = Input
    model = nb.attach_conv_layer(model, 32, summary = True)
    model = nb.attach_relu_layer(model)
    model = nb.attach_conv_layer(model, 32, summary = True)
    model = nb.attach_relu_layer(model)
    model = nb.attach_pooling_layer(model)

    model = nb.attach_conv_layer(model, 64, summary=True)
    model = nb.attach_relu_layer(model)
    model = nb.attach_conv_layer(model, 64, summary=True)
    model = nb.attach_relu_layer(model)
    model = nb.attach_pooling_layer(model)

    model = nb.attach_conv_layer(model, 128, summary=True)
    model = nb.attach_relu_layer(model)
    model = nb.attach_conv_layer(model, 128, summary=True)
    model = nb.attach_relu_layer(model)
    model = nb.attach_pooling_layer(model)

    model = nb.attach_flatten_layer(model)
    model = nb.attach_dense_layer(model, 200, summary = True)
    model = nb.attach_sigmoid_layer(model)
    model = nb.attach_dense_layer(model, 30, summary=True)
    model = nb.attach_sigmoid_layer(model)
    model = nb.attach_dense_layer(model, 2, summary=True)
    model = nb.attach_softmax_layer(model)
    prediction = model

with tf.name_scope("Optimization") as scope:
    global_itr = tf.Variable(0, name = "global_itr", trainable = False)
    cost = tf.nn.softmax_cross_entropy_with_logits(logits = prediction, labels = Target, name = "softmax_cost_function")
    cost = tf.reduce_mean(cost)
    tf.summary.scalar("cost", cost)

    optimizer = tf.train.AdamOptimizer().minimize(cost, global_step =global_itr)

with tf.name_scope("accuracy") as scope:
    correct_pred = tf.equal(tf.argmax(prediction, 1), tf.argmax(Target,1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

dg = DataSetGenerator("./train")

epochs = 10
batchsize = 10

saver = tf.train.Saver()
model_save_path = "./saved MyAwesomeModel/"
model_name = "model"

with tf.Session() as sess:
    summaryMerged = tf.summary.merge_all()

    filename = "./summary_log/run" + datetime.datetime.now().strftime(format = "%Y-%m-%d--%H-%M-%S")
    tf.global_variables_initializer().run()

    if os.path.exists(model_save_path+"checkpoint"):
        saver.restore(sess, tf.train.latest_checkpoint(model_save_path))
    writer = tf.summary.FileWriter(filename, sess.graph)

    for epoch in range(epochs):
        batches = dg.get_mini_batches(batchsize, (128,128), allchannel = False)
        for imgs, labels in batches:
            imgs = np.divide(imgs, 255)
            error, sumOut, acu, steps, _ = sess.run([cost, summaryMerged, accuracy, global_itr, optimizer],
                                                    feed_dict = {Input: imgs, Target: labels})
            writer.add_summary(sumOut, steps)
            print("epoch= ", epoch, "Total Samples Trained= ", steps*batchsize, "err=", error, "accuracy= ", acu)
            if steps%100 == 0:
                print("Saving the model")
                saver.save(sess, model_save_path+model_name, global_step = steps)