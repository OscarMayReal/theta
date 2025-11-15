import os from 'node:os';
import gtk from "@girs/node-gtk-4.0";
import { readFile } from 'node:fs/promises';
import Gio from '@girs/node-gio-2.0';

async function parseDistroInfo() {
    console.log("Parsing distro info");
    const data = await readFile('/etc/os-release', 'utf8')
    console.log(data);
    const lines = data.split('\n')
    const releaseDetails: { [key: string]: string } = {}
    lines.forEach((line, index) => {
        const words = line.split('=')
        releaseDetails[words[0].trim().toLowerCase()] = words[1]
    })
    return releaseDetails;
}

function ThisDeviceRow() {
    const box = new gtk.Box({
        orientation: gtk.Orientation.HORIZONTAL,
        spacing: 6,
    });
    const infoBox = new gtk.Box({
        orientation: gtk.Orientation.VERTICAL,
        spacing: 6,
    });
    var title = new gtk.Label({
        label: os.hostname(),
    });
    title.setCssClasses(["title-2"]);
    var subtitle = new gtk.Label({
        label: "test",
    });
    subtitle.setCssClasses(["caption"]);
    infoBox.append(title);
    infoBox.append(subtitle);
    box.append(infoBox);
    return box;
}

function ThisDevicePage() {
    const box = new gtk.Box({
        orientation: gtk.Orientation.VERTICAL,
        spacing: 6,
        visible: false,
    });
    box.connect("notify::visible", () => {
        parseDistroInfo().then((distroInfo) => {
            console.log(distroInfo);
        });
    });
    box.append(ThisDeviceRow());
    box.setVisible(true);
    return {
        content: box,
    }
}

export default {
    content: ThisDevicePage,
    title: "This Device",
    icon: "go-home-symbolic",
}
