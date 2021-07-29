def SetVersion(id, gc):
    actualVersion = '1.2.0'
    tabSellers = gc.open(
        "Solicitação de teste RoyalPlace (Respostas)").worksheet("Sellers")
    # print("id: ", id)
    coord = 'I'+str(id+2)
    # print("coord :", coord)
    tabSellers.update_acell(coord, actualVersion)