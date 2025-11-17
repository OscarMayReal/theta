import Image from "next/image";
import {Header} from "@/components/header";
import { Button } from "@/components/ui/button";
import { ArrowDownToLineIcon, InfoIcon } from "lucide-react";

export default function Home() {
  return (
    <div>
      <DownloadPageIntro />
      <Arm64DownloadSection />
      <X64DownloadSection />
    </div>
  );
}

function DownloadPageIntro() {
    return (
        <div className="page-intro-section" style={{
          height: "100px"
        }}>
            <div className="page-intro-section-inner">
                <div className="page-intro-subtitle-upper">Get Started</div>
                <div className="page-intro-title">Get Quntem ThetaOS</div>
                <div className="page-intro-subtitle-lower">Download The correct version for your device</div>
            </div>
        </div>
    )
}

function Arm64DownloadSection() {
    return (
        <div className="page-info-section">
            <div className="page-info-section-inner">
                <div className="page-info-section-content">
                  {/* <div className="page-info-section-subtitle">For Arm64 devices and VMs on Apple Silicon</div> */}
                  <div className="page-info-section-title">Quntem ThetaOS Arm64</div>
                  <div className="page-info-section-text">Download Quntem ThetaOS for Arm64 devices and VMs on Apple Silicon</div>
                </div>
                <div className="page-info-section-image" style={{
                  display: "flex",
                  flexDirection: "row",
                  justifyContent: "flex-end"
                }}>
                  <a href="https://github.com/OscarMayReal/grid/releases/download/ThetaOS_1.0.0/live-image-arm64.hybrid.iso"><Button variant="outline"><ArrowDownToLineIcon /> Download</Button></a>
                </div>
            </div>
        </div>
    )
}

function X64DownloadSection() {
    return (
        <div className="page-info-section">
            <div className="page-info-section-inner">
                <div className="page-info-section-content">
                  {/* <div className="page-info-section-subtitle">For Arm64 devices and VMs on Apple Silicon</div> */}
                  <div className="page-info-section-title">Quntem ThetaOS x64</div>
                  <div className="page-info-section-text">Download Quntem ThetaOS for x64 devices and VMs</div>
                </div>
                <div className="page-info-section-image" style={{
                  display: "flex",
                  flexDirection: "row",
                  justifyContent: "flex-end"
                }}>
                  <a href="https://github.com/OscarMayReal/grid/releases/download/ThetaOS_1.0.0/live-image-amd64.hybrid.iso"><Button variant="outline"><ArrowDownToLineIcon /> Download</Button></a>
                </div>
            </div>
        </div>
    )
}