import React from "react";
import {motion} from "framer-motion";

const ServiceCard:React.FC<{
  id:number;
  icon:string;
  onClick:() => void;
}> = ({id, icon, onClick}) => {
  return <>
    <motion.div
      layoutId={`card-${id}`}
      className="w-24 h-24 md:w-[150px] md:h-[150px] rounded-3xl bg-white outline-4 outline-[rgba(0,0,0,0.1)] shadow-[0_4px_2px_3px_rgba(0,0,0,0.25)] cursor-pointer"
      onClick={onClick}
      initial={{"y": 20, "opacity": 0}}
      whileHover={{
        "scale": 1.2,
        "rotate": id % 2 == 0 ? 10 : -10,
        transition: {
          type: "spring",
          duration: 0.2,
          bounce: 0.4,
          stiffness: 150
        }
      }}
      whileInView={{
        "y": 0,
        "opacity": 1,
        transition: {
          type: "spring",
          duration: 0.6,
          delay: id * 0.2,
          bounce: 0.4,
          stiffness: 150
        }
      }}
      >
      <div className="flex w-full h-full justify-center items-center">
        <img src={`/assets/emojis/${icon}.png`} className="w-16 md:w-32" />
      </div>
    </motion.div>
  </>;
}
export default ServiceCard;
