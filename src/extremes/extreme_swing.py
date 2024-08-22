import pandas as pd


# %%
# select ens and plev, where there are more than one extreme event in one year
def events_above_once(events):
    return events[
        events.groupby([events.start_time.dt.year, "ens", "plev"])["mean"].transform(
            "size"
        )
        > 1
    ]


# %%
def collect_swing(events, include_all=False):
    events = events.sort_values("extreme_start_time")

    all = []  # all cases
    pp = []  # positive + positive
    nn = []  # negative + negative
    pn = []  # positive + negative
    np = []  # negative + positive

    # more than one extreme event
    for i in range(len(events) - 1):
        first = events.iloc[i]
        second = events.iloc[i + 1]

        # occurrence of events more than twice
        all_ = []
        pp_ = []
        nn_ = []
        pn_ = []
        np_ = []

        all_ = update_swing(all_, first, second)

        if first.extreme_type == "pos" and second.extreme_type == "pos":
            pp_ = update_swing(pp_, first, second)
        elif first.extreme_type == "neg" and second.extreme_type == "neg":
            nn_ = update_swing(nn_, first, second)
        elif first.extreme_type == "pos" and second.extreme_type == "neg":
            pn_ = update_swing(pn_, first, second)
        elif first.extreme_type == "neg" and second.extreme_type == "pos":
            np_ = update_swing(np_, first, second)

        all_ = pd.DataFrame(all_)
        pp_ = pd.DataFrame(pp_)
        nn_ = pd.DataFrame(nn_)
        pn_ = pd.DataFrame(pn_)
        np_ = pd.DataFrame(np_)

        all.append(all_)
        pp.append(pp_)
        nn.append(nn_)
        pn.append(pn_)
        np.append(np_)

    all = pd.concat(all, axis=0)
    pp = pd.concat(pp, axis=0)
    nn = pd.concat(nn, axis=0)
    pn = pd.concat(pn, axis=0)
    np = pd.concat(np, axis=0)

    swing = pd.concat(
        [all, pp, nn, pn, np],
        axis=0,
        keys=["all", "pos_pos", "neg_neg", "pos_neg", "neg_pos"],
    )

    return swing


# %%
def update_swing(swing, first, second):
    swing.append(
        {
            "first_start_time": first.start_time,
            "first_end_time": first.end_time,
            "first_duration": first.duration,
            "second_start_time": second.start_time,
            "second_end_time": second.end_time,
            "second_duration": second.duration,
            "gap_duration": (second.start_time - first.end_time).days,
        }
    )
    return swing


# %%
def collect_noswing(events):

    return events[
        events.groupby([events.start_time.dt.year, "ens", "plev"])["mean"].transform(
            "size"
        )
        == 1
    ]
