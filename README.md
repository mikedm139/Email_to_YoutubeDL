# Email_to_YoutubeDL
A python script to check a designated inbox and pass URLs to youtube-dl. This was developed as an alternative to the now defunct "PlexIt!" service (RIP).

## Requirements
 * A Plex Media Server (technically this could be used to archive web videos without adding them to Plex)
 * An email account with IMAP and SMTP access

## Setup
 Download/Clone the git repo to the destination directory. While it's possible to run the python script directly, I recommend setting up inside it's own virtual environment to avoid dependency conflicts. 

### Steps
* Unzip the download archive and rename it as appropriate.
* Change directory into the folder
* Setup a python virtual environment `python3 -m venv venv`
* Copy the `config.template` file to `config` and edit the values for your setup:
  * Notes:
    * "allowed_senders": a list of email addresses that you wish to accept. If left empty, emails from any sender will be accepted -- Not recommended.
    * "youtube-dl options": arguments to pass to youtube-dl. See [youtube-dl project](https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L141) for details on available options
      * "outtmpl": should include both the path to the directory which Plex will scan for the downloaded videos as well as the format string for naming the downloaded file.
      * "download_archive": a path where the script should keep a list of downloaded files, to avoid wasting time and space downloading duplicates.
* Copy `execute.template` file to `execute.sh` and edit the paths for your setup.
* Add an entry to your crontab to run the execute.sh script at a reasonable period. I currently have mine set to run every half-hour. eg. `*/30 * * * * /path/to/Email_to_YoutubeDL/execute.sh`
