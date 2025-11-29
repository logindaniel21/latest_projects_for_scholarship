def get_v1(m1=None, u1=None, m2=None, u2=None):
    #u1 = abs(u1)
    #u2 = abs(u2)

    v1 = (((m1-m2)/(m1+m2))*u1) + (((2*m2)/(m1+m2))*u2)
    return v1

def get_v2(m1=None, u1=None, m2=None, u2=None):
    #u1 = abs(u1)
    #u2 = abs(u2)

    v2 = (((2*m1)/(m1+m2))*u1) + (((m2-m1)/(m2+m1))*u2)
    return v2


if __name__ == "__main__":
    print(get_v1(m1=10,m2=1,u1=2, u2=-5))
    print(get_v2(m1=10, m2=1, u1=2, u2=-5))