# [Convert Video](https://github.com/Cryden13/ConvertVideo)

A tool to help convert and compress video files with specified extensions (from config.ini) within a specified folder (and optionally its subfolders) to HEVC/AAC or VP9/OPUS.

**Requirements:**

[ffmpeg](https://www.ffmpeg.org/)  
[nircmd](https://www.nirsoft.net/utils/nircmd.html) (only for the context menu scripts)

## Usage

From command-line: py -m convertvideo \[PATH]

**Parameters:**

- *top_path* (str): The path to either a directory to be searched or a video file

## Changelog

<table>
    <tbody>
        <tr>
            <th align="center">Version</th>
            <th align="left">Changes</th>
        </tr>
        <tr>
            <td align="center">1.0</td>
            <td>Initial release</td>
        </tr>
        <tr>
            <td align="center">2.0</td>
            <td>
                <dl>
                    <dt>new</dt>
                    <ul>
                        <li>added additional methods</li>
                        <li>overhauled just about everything</li>
                    </ul>
                </dl>
            </td>
        </tr>
        <tr>
            <td align="center">2.1</td>
            <td>
                <dl>
                    <dt>new</dt>
                    <ul>
                        <li>combined ConvertVideo and CompressVideo for simplicity</li>
                        <li>added a bunch of customization</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>none👍</li>
                    </ul>
                </dl>
            </td>
        </tr>
        <tr>
            <td align="center">2.2</td>
            <td>
                <dl>
                    <dt>new</dt>
                    <ul>
                        <li>overhauled everything</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>fixed multiple errors</li>
                    </ul>
                </dl>
            </td>
        </tr>
        <tr>
            <td align="center">2.3</td>
            <td>
                <dl>
                    <dt>new</dt>
                    <ul>
                        <li>Now checks for subtitle language</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>Fixed selecting streams not working</li>
                    </ul>
                </dl>
            </td>
        </tr>
        <tr>
            <td align="center">3.0</td>
            <td>
                <dl>
                    <dt>new</dt>
                    <ul>
                        <li>Added a lot more options</li>
                        <li>Added a lot more info transparency</li>
                        <li>Added more options</li>
                        <li>Added more editable options in config</li>
                        <li>Added application icon</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>Now properly parses audio</li>
                        <li>Now properly parses subtitles</li>
                        <li>Stopped from attempting to convert previously converted items</li>
                        <li>App properly closes after completion</li>
                    </ul>
                </dl>
            </td>
        </tr>
        <tr>
            <td align="center">3.1</td>
            <td>
                <dl>
                    <dt>new</dt>
                    <ul>
                        <li>Added more info for transparency</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>Fixed error dealing with audio channels</li>
                    </ul>
                </dl>
            </td>
        </tr>
        <tr>
            <td align="center">3.2</td>
            <td>
                <dl>
                    <dt>new</dt>
                    <ul>
                        <li>Added even more info for transparency</li>
                        <li>Added the option to NOT convert streams</li>
                        <li>Added the option to add arguments</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>Fixed error that caused sequential files to not be properly processed</li>
                        <li>Fixed syntax error that caused issues with webms</li>
                    </ul>
                </dl>
            </td>
        </tr>
        <tr>
            <td align="center">4.0</td>
            <td>
                <dl>
                    <dt>new</dt>
                    <ul>
                        <li>Moved ConvertVideo from systemscripts to its own package</li>
                        <li>Added a check for duration comparison for better error checking</li>
                        <li>Console now automatically moves left or right from config option</li>
                        <li>Created powershell scripts that will add/remove 'Convert Video' to context menus (currently requires nircmd)</li>
                    </ul>
                </dl>
            </td>
        </tr>
        <tr>
            <td align="center">4.1</td>
            <td>
                <dl>
                    <dt>new</dt>
                    <ul>
                        <li>Added option to rename output using regex</li>
                        <li>Added option to keep all streams with languages that are in the config</li>
                        <li>Added config option for the duration checker</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>Stopped the reassignment of language metadata when there's only one stream and a language option was selected</li>
                        <li>Fixed the issue where the progressbar would keep getting wider by adding wordwrap</li>
                        <li>Fixed the index error when attempting to find audio/subtitle metadata</li>
                    </ul>
                </dl>
            </td>
        </tr>
    </tbody>
</table>
