# ThetaOS Netspace + ThetaOS Website

Warning: both of these are still in beta, and quite basic

# NetSpace

Netspace is a file sharing service that allows users to share files with others over the local network (computer that share the same physical space)

## Features

- Share files with others over the local network
- Upload and download files
- browse files

## Installation

### Backend
```bash
# cd netspace
npm install
```

### Frontend
```bash
# cd shell
uv sync
```

## Usage

### Backend
```bash
# cd netspace
npm run start
```

Edit the config.json file to add your shares. the format is as follows:
```json
{
    "exposedShares": [
        {
            "name": "Shared folder 1",
            "slug": "sharedf1",
            "path": "./sharedf1"
        }
    ]
}
```

name : the name of the share
slug : the slug of the share (used to identify the share)
path : the path of the folder to share

### Frontend
```bash
# cd shell
./shell
```

# Website

the new thetaOS website is designed to show the features of ThetaOS
