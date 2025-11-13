import express from "express";
import fs from "fs";
import path from "path";
import os from "os";

const app = express();
const port = 1526;
const space = "netspace"

type ExposedShare = {
    name: string;
    slug: string;
    path: string;
};

var exposedShares: ExposedShare[] = [
    {   
        name: "Shared folder 1",
        slug: "sharedf1",
        path: "./sharedf1",
    }
];

function formatExposedShare(share: ExposedShare) {
    return {
        name: share.name,
        slug: share.slug,
    };
}

function DiscoverNetwork() {
    const startIP = "192.168.1."
    const foundDevices: string[] = [];
    for (let i = 1; i <= 254; i++) {
        const ip = startIP + i;
        fetch(`http://${ip}:${port}/info`)
            .then((res) => res.json())
            .then((data) => {
                if (data.isNetSpace) {
                    console.log(`Found Netspace at ${ip}`);
                    foundDevices.push(ip);
                }
            })
            .catch((err) => {
                console.log(`Failed to connect to ${ip}`);
            });
    }
    return foundDevices;
}

app.get("/info", (req, res) => {
    const info = {
        isNetSpace: true,
        netspace: {
            space,
            version: "1.0.0",
            capabilities: {
                fileShare: {
                    status: "enabled",
                }
            }
        }
    };
    res.json(info);
});

app.get("/cap/fileshare", (req, res) => {
    const fileshare = {
        status: "enabled",
        exposedShares: exposedShares.map(formatExposedShare),
    };
    res.json(fileshare);
});

app.get("/cap/fileshare/share/:shareSlug/files", (req, res) => {
    const shareSlug = req.params.shareSlug;
    const share = exposedShares.find((share) => share.slug === shareSlug);
    if (!share) {
        res.status(404).json({ error: "Share not found" });
        return;
    }
    const files = fs.readdirSync(share.path);
    const formattedFiles = files.map((file) => {
        return {
            name: file,
            path: path.join(share.path, file),
        };
    });
    res.json({
        files: formattedFiles,
    });
});

app.listen(port, () => {
    console.log(`Netspace listening on port ${port}`);
    const foundDevices = DiscoverNetwork();
    console.log(`Found ${foundDevices.length} devices`);
});
