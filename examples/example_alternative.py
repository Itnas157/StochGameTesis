init_vars = ["t=0", "x=0", "y=0"]
trans_str = """
t=0 ^ x=0 ^ y=0 -> 0.5:x=1,t=1 0.5:x=0,t=1 !no_traiciona;
t=0 ^ x=0 ^ y=0 -> 0.5:x=2,t=1 0.5:x=0,t=1 !traiciona;

t=0 ^ y=1 ^ x=0 -> 1:x=1,_R_=3 !no_traiciona;
t=0 ^ y=1 ^ x=0 -> 1:x=2,_R_=4 !traiciona;
t=0 ^ y=2 ^ x=0 -> 1:x=1,_R_=2 !no_traiciona;
t=0 ^ y=2 ^ x=0 -> 1:x=2,_R_=1 !traiciona;

t=1 ^ y=0 ^ x=0 -> 0.5:y=1,t=0 0.5:y=0,t=0 !no_traiciona;
t=1 ^ y=0 ^ x=0 -> 0.5:y=2,t=0 0.5:y=0,t=0 !traiciona;

t=1 ^ x=1 ^ y=0 -> 1:y=1,_R_=3 !no_traiciona;
t=1 ^ x=1 ^ y=0 -> 1:y=2,_R_=2 !traiciona;
t=1 ^ x=2 ^ y=0 -> 1:y=1,_R_=4 !no_traiciona;
t=1 ^ x=2 ^ y=0 -> 1:y=2,_R_=1 !traiciona;
"""