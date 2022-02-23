from avlslideshow import AVL_Slideshow

data = [467, 768, 546, 893, 490, 217, 562, 386, 998, 436, 881, 235, 453, 478]
tree = AVL_Slideshow(data=data)

cycle = [943, 307, 832, 673, 139]
for x in cycle:
    tree.add(x)
for x in cycle:
    tree.delete(x)
tree.show()
