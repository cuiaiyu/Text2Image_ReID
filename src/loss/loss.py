import torch
import numpy as np

def cos_distance(x,y):
    eps = 1e-12
    dot_prod = np.dot(x,y.transpose(1,0))
    x_norm = np.linalg.norm(x, axis=1, keepdims=True)
    y_norm = np.linalg.norm(y, axis=1, keepdims=True)
    tmp = dot_prod / (np.dot(x_norm, y_norm.transpose(1,0)) + eps)
    return 1 - tmp


def triplet_cos_loss(x, pos, neg, margin=0.2):
    def cos_dist(x,y):
        # import pdb; pdb.set_trace()
        return 1 - torch.sum(x*y, 1) / (torch.norm(x, dim=1)*torch.norm(y, dim=1))
    pos_dist = cos_dist(x, pos)
    neg_dist = cos_dist(x, neg)
    scores = torch.clamp(pos_dist - neg_dist + margin, min=0)
    return scores.mean()


def crossmodal_triplet_loss_new(img, pos_img, neg_img, cap, pos_cap, neg_cap, triplet_loss, dist_fn_opt):
    loss = 0.0
    loss = loss + triplet_loss(img, pos_img, neg_img)
    loss = loss + triplet_loss(cap, pos_cap, neg_cap)
    loss = loss + triplet_loss(img, cap, neg_cap)
    loss = loss + triplet_loss(cap, img, neg_img)
        
    return loss

def crossmodal_triplet_loss(img, pos_img, neg_img, cap, pos_cap, neg_cap, triplet_loss, dist_fn_opt):
    loss = 0.0
    if True: #dist_fn_opt == "euclidean":
        loss = loss + triplet_loss(img, pos_img, neg_img)
        loss = loss + triplet_loss(cap, pos_cap, neg_cap)

        loss = loss + triplet_loss(img, pos_cap, neg_cap)
        loss = loss + triplet_loss(img, pos_cap, neg_img)
        loss = loss + triplet_loss(img, pos_img, neg_cap)
        loss = loss + triplet_loss(cap, pos_img, neg_img)
        loss = loss + triplet_loss(cap, pos_img, neg_cap)
        loss = loss + triplet_loss(cap, pos_cap, neg_img)

        loss = loss + triplet_loss(cap, img, neg_cap)
        loss = loss + triplet_loss(cap, img, neg_img)
        
    elif dist_fn_opt == "cosine":
        same = torch.Tensor(img.size(0)).fill_(1).cuda()
        diff = torch.Tensor(img.size(0)).fill_(-1).cuda()
        
        loss = loss + triplet_loss(img, cap, same)
        loss = loss + triplet_loss(img, img, same)
        loss = loss + triplet_loss(pos_img, pos_cap, same)

        loss = loss + triplet_loss(img, neg_img, diff)
        loss = loss + triplet_loss(cap, neg_img, diff)
        loss = loss + triplet_loss(img, neg_cap, diff)
        loss = loss + triplet_loss(cap, neg_cap, diff)

        loss = loss + triplet_loss(pos_img, neg_img, diff)
        loss = loss + triplet_loss(pos_cap, neg_img, diff)
        loss = loss + triplet_loss(pos_img, neg_cap, diff)
        loss = loss + triplet_loss(pos_cap, neg_cap, diff)
    return loss