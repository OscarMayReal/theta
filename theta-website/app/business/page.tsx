import Image from "next/image";
import {Header} from "@/components/header";

export default function Home() {
  return (
    <div>
      <BusinessPageIntro />
    </div>
  );
}

function BusinessPageIntro() {
    return (
        <div className="page-intro-section">
            <div className="page-intro-section-inner">
                <div className="page-intro-subtitle-upper">ThetaOS Business</div>
                <div className="page-intro-title">Simple, powerful fleet management with Grid</div>
            </div>
        </div>
    )
}