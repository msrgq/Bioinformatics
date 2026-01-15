import numpy as np

def predict_steps(M, v0, steps=5, as_row_vector=True, normalize=False):
    M = np.array(M, dtype=float)
    v = np.array(v0, dtype=float)

    n = M.shape[0]
    if M.shape != (n, n):
        raise ValueError("M must be square (n x n).")
    if v.shape not in [(n,), (n, 1)]:
        raise ValueError(f"v0 must have length {n}.")

    v = v.reshape(-1)

    history = [v.copy()]
    for _ in range(steps):
        v = (v @ M) if as_row_vector else (M @ v)

        if normalize:
            s = v.sum()
            if s != 0:
                v = v / s

        history.append(v.copy())

    return history

def predict_5_steps(M, v0, as_row_vector=True, normalize=False):
    return predict_steps(M, v0, steps=5, as_row_vector=as_row_vector, normalize=normalize)


if __name__ == "__main__":
    M = [
        [0.7, 0.3],
        [0.2, 0.8]
    ]
    v0 = [1.0, 0.0]

    hist = predict_5_steps(M, v0, as_row_vector=True, normalize=True)

    for t, vt in enumerate(hist):
        print(f"v{t} = {vt}")
    print("\nPrediction after 5 steps:", hist[-1])
