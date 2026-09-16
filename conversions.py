def cmyk_gcr(c, m, y):
    k = min(c, m, y)

    if k >= 1:
        return 0.0, 0.0, 0.0, 1.0

    c = (c - k) / (1 - k)
    m = (m - k) / (1 - k)
    y = (y - k) / (1 - k)

    return c, m, y, k


def cmyk_ucr(c, m, y, threshold=0.5):
    k_raw = min(c, m, y)

    if k_raw <= threshold:
        k = 0.0
    else:
        k = k_raw * (k_raw - threshold) / (1 - threshold)

    c -= k
    m -= k
    y -= k

    return c, m, y, k


def rgb_to_cmyk(r, g, b, method="GCR", ucr_threshold=50.0):
    r = float(r) / 255
    g = float(g) / 255
    b = float(b) / 255

    c = 1 - r
    m = 1 - g
    y = 1 - b

    if method == "GCR":
        c, m, y, k = cmyk_gcr(c, m, y)

    elif method == "UCR":
        threshold = float(ucr_threshold) / 100
        c, m, y, k = cmyk_ucr(c, m, y, threshold)

    else:
        raise ValueError("Unknown CMYK separation method")

    return c * 100, m * 100, y * 100, k * 100


def cmyk_to_rgb(c, m, y, k):
    c = float(c) / 100
    m = float(m) / 100
    y = float(y) / 100
    k = float(k) / 100

    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)

    return r, g, b


def rgb_to_hsv(r, g, b):
    r = float(r) / 255
    g = float(g) / 255
    b = float(b) / 255

    maximum = max(r, g, b)
    minimum = min(r, g, b)
    delta = maximum - minimum

    v = maximum

    if maximum == 0:
        s = 0
    else:
        s = delta / maximum

    if delta == 0:
        h = 0
    elif maximum == r:
        h = 60 * (((g - b) / delta) % 6)
    elif maximum == g:
        h = 60 * (((b - r) / delta) + 2)
    else:
        h = 60 * (((r - g) / delta) + 4)

    return h, s * 100, v * 100


def hsv_to_rgb(h, s, v):
    h = float(h)
    s = float(s) / 100
    v = float(v) / 100

    h = h % 360

    if s == 0:
        r = v
        g = v
        b = v
        return r * 255, g * 255, b * 255

    h_sector = h / 60
    i = int(h_sector)
    f = h_sector - i

    m = v * (1 - s)
    n = v * (1 - s * f)
    k = v * (1 - s * (1 - f))

    if i == 0:
        r, g, b = v, k, m
    elif i == 1:
        r, g, b = n, v, m
    elif i == 2:
        r, g, b = m, v, k
    elif i == 3:
        r, g, b = m, n, v
    elif i == 4:
        r, g, b = k, m, v
    else:
        r, g, b = v, m, n

    return r * 255, g * 255, b * 255


def rgb_to_all(r, g, b, method="GCR"):
    return {
        "RGB": (float(r), float(g), float(b)),
        "CMYK": rgb_to_cmyk(r, g, b, method=method),
        "HSV": rgb_to_hsv(r, g, b),
    }


def cmyk_to_all(c, m, y, k, method="GCR"):
    rgb = cmyk_to_rgb(c, m, y, k)
    return {
        "RGB": tuple(float(x) for x in rgb),
        "CMYK": rgb_to_cmyk(*rgb, method=method),
        "HSV": rgb_to_hsv(*rgb),
    }


def hsv_to_all(h, s, v):
    rgb = hsv_to_rgb(h, s, v)
    return rgb_to_all(*rgb)