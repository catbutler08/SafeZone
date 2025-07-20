import React from "react";
import {AnimatePresence, motion} from "framer-motion";
import {ChevronDown, ChevronRight} from "lucide-react";
import Button from "../components/atoms/button";
import ServiceCard from "../components/organisms/ServiceCard";

interface Service{
  icon:string;
  title:string;
  description:string;
}

const services:Service[] = [
  {icon: "round_pushpin", title: "위치를 확인할 수 있어요.", description: "실시간으로 Google Maps API를 활용한 지도 위에서 피보호자의 위치를 확인할 수 있어요."},
  {icon: "police_car", title: "알람을 받을 수 있어요.", description: "설정된 안전 구역을 이탈할 경우, 보호자에게 알람을 보냅니다."},
  {icon: "bookmark", title: "어디로 이동하였는지 알 수 있어요.", description: "시간대 별로 어디에 위치하였는지 알 수 있어요."}
];

const Main:React.FC = () => {
  const [selectedCard, setSelectedCard] = React.useState<number|null>(null);

  React.useLayoutEffect(() => {
    document.documentElement.classList.add("h-full", "overflow-y-scroll", "snap-y", "snap-mandatory", "scroll-hide");
    return () => {
      document.documentElement.classList.remove("h-full", "overflow-y-scroll", "snap-y", "snap-mandatory", "scroll-hide");
    };
  }, []);

  const handleCardClick = React.useCallback((id:number) => () => {
    setSelectedCard(id);
  }, []);

  return (
    <div>
      <section className="relative h-screen snap-start">
        <div className="h-screen bg-position-[-150px] bg-no-repeat bg-cover bg-[url(/assets/background/main.jpg)] grayscale-100 md:bg-center">
          <div className="flex flex-col items-center text-white text-center px-20 pt-[120px] md:block md:text-left md:pt-56 md:pl-48 md:pr-0">
            <div className="font-black text-3xl md:text-5xl">Safe Zone</div>
            <div className="mt-5 font-medium text-2xl md:text-4xl">당신의 부모님을 안전하게</div>
            <Button className="max-w-[40px] mt-12 gap-1">지금 해보기 <ChevronRight /></Button>
          </div>
        </div>
        <motion.div
          className="absolute bottom-[2px] left-1/2 translate-x-[-50%]"
          initial={{"bottom": "2px", "opacity": 1}}
          animate={{"bottom": "-12px", "opacity": 0}}
          transition={{
            duration: 0.8,
            repeat: Infinity,
            repeatDelay: 1
          }}
          >
            <ChevronDown size={96} color="white" />
        </motion.div>
      </section>
      <section className="relative h-screen snap-start">
        <div className="pt-[20px] ml-[20px] text-2xl font-medium">주요 서비스</div>
        <div className="absolute top-1/2 translate-y-[-50%] flex flex-col md:flex-row gap-8 w-full justify-center items-center">
          {services.map((item, i) => <ServiceCard id={i} icon={item.icon} onClick={handleCardClick(i)} key={item.title} />)}
          <AnimatePresence>
            {(selectedCard !== null) && <motion.div
              layoutId={`card-${selectedCard}`}
              className="absolute top-1/2 translate-y-[-50%] w-[300px] md:w-[800px] h-[200px] overflow-hidden flex flex-row rounded-3xl bg-white outline-4 outline-[rgba(0,0,0,0.1)] shadow-[0_4px_2px_3px_rgba(0,0,0,0.25)] cursor-pointer"
              onClick={() => setSelectedCard(null)}
              >
                <motion.div
                  className="fixed scale-[300%] rotate-12 bottom-12 left-5 blur-[2px] -z-10 md:static md:scale-100 md:rotate-0 md:blur-none md:flex md:h-full md:ml-10 md:mr-5 md:justify-center md:items-center"
                  initial={{"y": 40, "opacity": 0}}
                  animate={{"y": 0, "opacity": 1}}
                  whileHover={{"rotate": -10, "scale": 1.2}}
                  transition={{type: "spring", duration: 0.4}}
                  >
                  <img src={`/assets/emojis/${services[selectedCard].icon}.png`} className="w-16 md:w-32" />
                </motion.div>
                <div className="flex flex-col ml-5 md:ml-0 mr-5 justify-center text-black gap-5">
                  <motion.span
                    className="font-semibold text-xl md:text-2xl"
                    initial={{"y": 10, "opacity": 0}}
                    animate={{"y": 0, "opacity": 1}}
                    transition={{type: "spring", duration: 1.2, delay: 0.3}}
                    >
                    {services[selectedCard].title}
                    </motion.span>
                  <motion.span
                    className="text-lg md:text-xl"
                    initial={{"y": 10, "opacity": 0}}
                    animate={{"y": 0, "opacity": 1}}
                    transition={{type: "spring", duration: 1.2, delay: 0.6}}
                    >
                    {services[selectedCard].description}
                  </motion.span>
                </div>
            </motion.div>}
          </AnimatePresence>
        </div>
      </section>
    </div>
  );
};
export default Main;
