#!/usr/bin/env python3
import fire
import json
import os
import numpy as np
import tensorflow.compat.v1 as tf
from pathlib import Path
from runModel import model, sample, encoder

nsamples = None
batch_size=None
context= None
sess = None
output = None
enc = None
hparams=None
c=Path(__file__).parents[0]
m = c / 'models'
m=str(m)

def interact_model(input) -> str:
    model_name='bott'
    seed=None
    global nsamples
    nsamples=1
    global batch_size
    batch_size=1
    length=None
    temperature=1
    top_k=0
    top_p=1
    models_dir=m

    models_dir = os.path.expanduser(os.path.expandvars(models_dir))
    if batch_size is None:
        batch_size = 1
    assert nsamples % batch_size == 0
        
    global enc 
    enc = encoder.get_encoder(model_name, models_dir)
    hparams = model.default_hparams()
    with open(os.path.join(models_dir, model_name, 'hparams.json')) as f:
        hparams.override_from_dict(json.load(f))


    if length is None:
        length = hparams.n_ctx // 2
    elif length > hparams.n_ctx:
        raise ValueError("Can't get samples longer than window size: %s" % hparams.n_ctx)
        
    with tf.Session(graph=tf.Graph()) as sess2:
        global sess
        sess=sess2
        global context
        context = tf.placeholder(tf.int32, [batch_size, None])
        np.random.seed(seed)
        tf.set_random_seed(seed)
        global output
        output = sample.sample_sequence(
        hparams=hparams, length=length,
        context=context,
        batch_size=batch_size,
        temperature=temperature, top_k=top_k, top_p=top_p)
        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join(models_dir, model_name))
        saver.restore(sess, ckpt)
        
        raw_text = input
        context_tokens = enc.encode(raw_text)
        for _ in range(nsamples // batch_size):
            out = sess.run(output, feed_dict={ context: [context_tokens for _ in range(batch_size)]})[:, len(context_tokens):]
            for i in range(batch_size):
                text = enc.decode(out[i])
        return text            

if __name__ == '__main__':
    fire.Fire(interact_model)
