import json
import os

songs = []

files = [dr for dr in os.listdir("Spotify Extended Streaming History") if dr.split(".")[1] == "json" and "Video" not in dr]

for f in files:
    with open(f"Spotify Extended Streaming History/{f}", errors="ignore") as file:
        data = json.load(file)
        for i in data:
            songs.append(i)


def total_time(stats: list[dict]) -> str:
    time = 0
    for s in stats:
        time += s["ms_played"]
    total_seconds = time/1000
    hours = total_seconds // 3600
    remaining = total_seconds % 3600
    minutes = remaining // 60
    seconds = remaining % 60
    return f"{hours:.0f}h, {minutes:.0f}m, {seconds:.0f}s"


def skipped(stats: list[dict]) -> list[tuple]:
    skipper = {}
    for s in stats:
        if s["skipped"]:
            if s["master_metadata_track_name"] in skipper:
                skipper[s["master_metadata_track_name"]] += 1
            else:
                skipper[s["master_metadata_track_name"]] = 1

    return sorted(skipper.items(), key=lambda x: x[1], reverse=True)


def artist_group(stats: list[dict]) -> dict:
    """
    :param stats:
    :return: A dictionary with every song played sorted into artist categories
    """
    artists = {}
    for s in stats:
        name = s["master_metadata_album_artist_name"]
        if name:
            if name not in artists:
                artists[name] = [s]
            else:
                artists[name].append(s)
    return artists


def artist_listens(stats: dict) -> list:
    """
    :param stats:
    :return: A list containing the artists and their times listened in a tuple
    """
    artist_data = {}
    for s in stats:
        name = s
        value = len(stats[s])
        artist_data[name] = value
    return sorted(artist_data.items(), key=lambda x: x[1], reverse=True)


def artist_time(stats: dict) -> list:
    """
    :param stats:
    :return: A sorted list of the total playtime for every artist
    """
    artist_data = {}
    for s in stats:
        name = s
        value = sum([i["ms_played"]/1000 for i in stats[s]])
        artist_data[name] = value
    return sorted(artist_data.items(), key=lambda x: x[1], reverse=True)



def song_time(stats: list[dict]) -> list[tuple]:
    """
    :param stats:
    :return: A list of the name of a song along with how many times it has been listened to
    """
    artists = {}
    for s in stats:
        if s["master_metadata_track_name"]:
            if s["master_metadata_track_name"] in artists:
                artists[s["master_metadata_track_name"]] += s["ms_played"]//1000
            else:
                artists[s["master_metadata_track_name"]] = s["ms_played"]//1000
    return sorted(artists.items(), key=lambda x: x[1], reverse=True)


def song_listens(stats: list[dict]) -> list:
    """
    :param stats:
    :return: A sorted list of every time an artist has been listened to
    """
    artists = {}
    for s in stats:
        name = s["master_metadata_track_name"]
        if name:
            if name in artists:
                artists[name] += 1
            else:
                artists[name] = 1
    return sorted(artists.items(), key=lambda x: x[1], reverse=True)


def full_listens(stats: list[dict]) -> list:
    artists = {}
    for s in stats:
        name = s["master_metadata_track_name"]
        if name:
            if name in artists:
                artists[name] += 1
            else:
                artists[name] = 1

            if s["reason_end"] != "endplay" and name in artists:
                artists[name] -= 1

            if artists[name] < 0 and name in artists:
                artists[name] = 0
    return sorted(artists.items(), key=lambda x: x[1], reverse=True)


most_listened = song_listens(songs)
longest_listened = song_time(songs)
fully = full_listens(songs)

skip = skipped(songs)

artists = artist_group(songs)
most_artists = artist_listens(artists)
longest_artists = artist_time(artists)

total = total_time(songs)

with open("info.txt", "w") as output:
    print(file=output)
    print(f"{' Top 10 most listened ':#^50}", file=output)
    for i in range(10):
        print(f"#{f'{i+1}: {most_listened[i][0]}, {most_listened[i][1]}':^48}#", file=output)
    print("#"*50, file=output)
    print("\n", file=output)

    print(f"{' Top 10 longest listening times ':#^50}", file=output)
    for i in range(10):
        print(f"#{f'{i+1}: {longest_listened[i][0]}, {longest_listened[i][1]/60:.1f} min':^48}#", file=output)
    print("#" * 50, file=output)
    print("\n", file=output)

    print(f"{' Top 10 artists (listens) ':#^50}", file=output)
    for i in range(10):
        print(f"#{f'{i + 1}: {most_artists[i][0]}, {most_artists[i][1]}':^48}#", file=output)
    print("#" * 50, file=output)
    print("\n", file=output)

    print(f"{' Top 10 artists (time) ':#^50}", file=output)
    for i in range(10):
        print(f"#{f'{i + 1}: {longest_artists[i][0]}, {longest_artists[i][1]/60:.1f} min':^48}#", file=output)
    print("#" * 50, file=output)
    print("\n", file=output)

    print(f"{' Top 10 most skipped songs ':#^50}", file=output)
    for i in range(10):
        print(f"#{f'{i + 1}: {skip[i][0]}, {skip[i][1]}':^48}#", file=output)
    print("#" * 50, file=output)
    print("\n", file=output)

    print(f"{' Top 10 most fully listened songs ':#^50}", file=output)
    for i in range(10):
        print(f"#{f'{i + 1}: {fully[i][0]}, {fully[i][1]}':^48}#", file=output)
    print("#" * 50, file=output)
    print("\n", file=output)

    print(f"{' Total listening time ':#^50}", file=output)
    print(f"#{f'{total:^48}'}#", file=output)
    print("#"*50, file=output)
