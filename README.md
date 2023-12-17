# [Convert Video](https://github.com/Cryden13/ConvertVideo)

A tool to help convert and compress video files with specified extensions (from config.ini) within a specified folder (and optionally its subfolders) to HEVC/AAC or VP9/OPUS.

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
                        <li>added a bunch of customization to ConvertVideo</li>
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
                        <li>overhauled ConvertVideo</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>fixed ConvertVideo errors</li>
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
                        <li>ConvertVideo checks for subtitle language</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>Fixed selecting streams in ConvertVideo not working</li>
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
                        <li>Added a lot more options for ConvertVideo</li>
                        <li>Added a lot more info transparency in ConvertVideo</li>
                        <li>Added more options for ConvertVideo</li>
                        <li>Added more editable options for ConvertVideo in config</li>
                        <li>Added application icon for ConvertVideo</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>ConvertVideo properly parses audio</li>
                        <li>ConvertVideo properly parses subtitles</li>
                        <li>Stopped ConvertVideo from attempting to convert previously converted items</li>
                        <li>ConvertVideo properly closes after completion</li>
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
                        <li>Added more info for transparency in ConvertVideo</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>Fixed error in ConvertVideo dealing with audio channels</li>
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
                        <li>Added even more info for transparency in ConvertVideo</li>
                        <li>Added the option to NOT convert streams in ConvertVideo</li>
                        <li>Added the option to add arguments in ConvertVideo</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>Fixed error in ConvertVideo that caused sequential files to not be properly processed</li>
                        <li>Fixed syntax error in ConvertVideo that caused issues with webms</li>
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
    </tbody>
</table>
