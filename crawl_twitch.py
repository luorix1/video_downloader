import argparse
import m3u8
import os
import ffmpeg
import re
import csv
from twitchdl import twitch


def get_full_link_m3u8_link(video_id):
  access_token = twitch.get_access_token(video_id)
  playlists_m3u8 = twitch.get_playlists(video_id, access_token)
  playlists = m3u8.loads(playlists_m3u8)
  for link in playlists.playlists:
    if link.stream_info.resolution is not None and link.stream_info.resolution[1] == 360:
      return link.uri
 
  return ''

def search(streamer, video_id, output_dir):
  download_url = get_full_link_m3u8_link(video_id)
  print(download_url)
  if download_url == '':
    print('Error at downloading video: ', streamer, video_id)

  stream = ffmpeg.input(download_url)
  stream = ffmpeg.output(stream, output_dir + '/' + streamer + '/video/' + streamer + '_' + video_id + '.mp4')
  ffmpeg.run(stream)
  return


def escape_ansi(line):
  ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
  return ansi_escape.sub('', line)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--output_dir', default='/data/data1/twitch',
                      help='directory to save video in')
  parser.add_argument('--streamer', default='zilioner',
                      help='twitch streamer to crawl')
  
  args = parser.parse_args()
  is_exist = os.path.exists(args.output_dir)
  if is_exist == False:
    os.makedirs(args.output_dir)
  is_exist_streamer = os.path.exists(args.output_dir + '/' + args.streamer)
  if is_exist_streamer == False:
    os.makedirs(args.output_dir + '/' + args.streamer)
    os.makedirs(args.output_dir + '/' + args.streamer + '/video')

  stream = os.popen('twitch-dl videos ' + args.streamer +' -l 50')
  output = stream.read()
  output_list = output.split('\n')
  link_list = []
  read_file = open('./twitch_videos.csv', 'r', encoding='utf-8')
  reader = csv.reader(read_file)
  downloaded_video_ids = []
  for video_info in reader:
    if video_info[0] == args.streamer:
      downloaded_video_ids.append(video_info[1])

  count = 0
  write_file = open('./twitch_videos.csv', 'a', encoding='utf-8')
  writer = csv.writer(write_file)
  for string in output_list:
    if string.find('https') >= 0:
      escape_ansi_string = escape_ansi(string)
      video_id = escape_ansi_string.split('/')[-1]
      if video_id not in downloaded_video_ids:
        search(args.streamer, video_id, args.output_dir)
        writer.writerow([args.streamer, video_id])
        print('Download completed: ', args.streamer, video_id)
  write_file.close()
