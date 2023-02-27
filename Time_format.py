def add_zero(num):
    return f"0{num}" if num < 10 else num

def s_in_m_h(all_time):
    s = all_time % 60
    m = (all_time // 60) % 60
    h = all_time // 3600   

    return s, m, h

def h_m_in_s(h, m, s):
    h_in_s = h * 3600
    m_in_s = m * 60

    seconds = h_in_s + m_in_s + s

    return seconds