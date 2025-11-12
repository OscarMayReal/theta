import Image from "next/image";
import {Header} from "@/components/header";
import { Button } from "@/components/ui/button";
import { InfoIcon, SquareArrowOutUpRightIcon } from "lucide-react";

export default function Home() {
  return (
    <div>
      <BusinessPageIntro />
      <EnrollmentInfoSection />
    </div>
  );
}

function BusinessPageIntro() {
    return (
        <div className="page-intro-section">
            <div className="page-intro-section-inner">
                <div className="page-intro-subtitle-upper">ThetaOS Business + Quntem Grid</div>
                <div className="page-intro-title">Simple, powerful fleet management with ThetaOS</div>
                <div className="page-intro-subtitle-lower">Control devices, deploy software, and monitor your fleet with ease</div>
                <div className="page-intro-button-row">
                  <Button variant="outline"><SquareArrowOutUpRightIcon /> Get Started</Button>
                  <Button variant="outline"><InfoIcon /> Learn More</Button>
                </div>
            </div>
        </div>
    )
}

function EnrollmentInfoSection() {
    return (
        <div className="page-info-section">
            <div className="page-info-section-inner">
                <div className="page-info-section-content">
                  <div className="page-info-section-subtitle">Enrollment</div>
                  <div className="page-info-section-title">Effortless Self-Enrollment</div>
                  <div className="page-info-section-text">Users self-enroll their devices with a Managed Quntem Account, no IT work required</div>
                </div>
                <img src="/self-enrollment.png" className="page-info-section-image" />
            </div>
        </div>
    )
}