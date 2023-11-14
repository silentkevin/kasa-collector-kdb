import os
import time

from pydub import AudioSegment

input_dir = "/Users/kbrown/tmp5/HP4"
book_num = 4
max_disks = 17

for i in range(1, max_disks + 1):
    output_path = os.path.join(input_dir, f"HP{book_num}_Disk_{i:02d}.mp3")
    print(f"output_path={output_path} exists {os.path.exists(output_path)}")

    if not os.path.exists(output_path):
        current_dir = os.path.join(input_dir, str(i))
        print(f"starting current_dir={current_dir},output_path={output_path}")

        mp3_file_list = sorted(os.listdir(current_dir))
        mp3_segments = []
        for mp3_file in mp3_file_list:
            full_mp3_file_path = os.path.join(current_dir, mp3_file)
            print(f"loading mp3 file {full_mp3_file_path}")
            segment: AudioSegment = AudioSegment.from_mp3(full_mp3_file_path)
            mp3_segments.append(segment)
            print(f"loaded mp3 file {full_mp3_file_path} with duration {segment.duration_seconds}")

        print(f"starting join")
        output: AudioSegment = AudioSegment.silent(duration=1000)
        for mp3_segment in mp3_segments:
            output = output + mp3_segment
            output = output + AudioSegment.silent(duration=2000)
        print(f"output length is {output.duration_seconds:,}")

        print(f"starting export to {output_path}")
        output.export(output_path, bitrate='128', format="mp3")
        print(f"done current_dir={current_dir}")

    cmd = f"id3tag -1 -2 -a'HP' -s'HP Book {book_num} Disk {i:02d}' -t{i} -T{max_disks} {output_path}"
    os.system(cmd)

    time.sleep(2)

    cmd = f"id3info {output_path}"
    os.system(cmd)
