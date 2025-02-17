import pandas as pd

def calculation(input_data:int):
    # change column
    change = []
    for i in range(0, len(input_data)):
      if i != 0:
        prev = input_data[i - 1]
        curr = input_data[i]
        val = curr - prev
        change.append(val)
      else:
        change.append(0)

    # gain
    gain = []
    for i in range(0, len(change)):
        if change[i] > 0:
            gain.append(change[i])
        else:
            gain.append(0)

    # loss
    loss = []
    for i in range(0, len(change)):
        if change[i] < 0:
            val = change[i]
            val = val * (-1)
            loss.append(val)
        else:
            loss.append(0)

    # avg gain
    avg_gain = []
    gain_sum = 0
    for i in range(3, 16):
        val = gain[i]
        gain_sum = gain_sum + val

    for i in range(1, 16):
        avg_gain.append(0)

    avg_gain.append(gain_sum / 14)

    for i in range(16, len(gain)):
        if len(avg_gain) >= 1:
            prev = avg_gain[-1]
            gain_val = gain[i - 1]
            val = ((prev * 13) + gain_val) / 14
            avg_gain.append(val)


    # avg loss
    avg_loss = []
    loss_sum = 0

    for i in range(3, 16):
        val = loss[i]
        loss_sum = loss_sum + val

    for i in range(1, 16):
        avg_loss.append(0)

    avg_loss.append(loss_sum / 14)

    for i in range(16, len(loss)):
        if len(avg_loss) >= 1:
            prev = avg_loss[-1]
            loss_val = loss[i - 1]
            val = ((prev * 13) + loss_val) / 14
            avg_loss.append(val)


    # hm
    hm = []
    for i in range(1, 16):
        hm.append(0)
    for i in range(15, len(input_data)):
        gain_val = avg_gain[i]
        loss_val = avg_loss[i]

        if loss_val == 0:
            val = gain_val / 1
            hm.append(val)
        else:
            val = gain_val / loss_val
            hm.append(val)

    # hma
    hma = []
    for i in range(1, 16):
        hma.append(0)

    for i in range(15,len(input_data)):
        if avg_loss[i] == 0:
            hma.append(100)
        else:
            val = hm[i]
            hma.append(100 - (100 / (1 + val)))

    df = pd.DataFrame({"input": input_data,
                       "change": change,
                       "gain": gain,
                       "loss": loss,
                       "avg-gain": avg_gain,
                       "avg-loss": avg_loss,
                       "hm": hm,
                       "hma": hma
                       })


    return df




