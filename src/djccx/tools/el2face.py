def el2face(el,nface=None):
    face_1 = el[[0,1,2]]
    face_2 = el[[0,3,1]]
    face_3 = el[[1,3,2]]
    face_4 = el[[2,3,0]]

    faces = [face_1,face_2,face_3,face_4]
    if nface is not None:
        return [faces[nface]]
    return faces
