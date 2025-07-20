import {motion} from "framer-motion";
import {twMerge} from "tailwind-merge";

const Button:React.FC<{
  className?:string;
  children:React.ReactNode[];
}> = ({className, children}) => {
  return <motion.button
    className={twMerge("flex justify-center items-center min-w-[200px] min-h-[50px] text-center text-black text-xl px-6 py-1 bg-[rgba(255,255,255,0.2)] outline-1 outline-[rgba(0,0,0,0.2)] rounded-xl backdrop-blur-[2px] cursor-pointer", className)}
    style={{
      "boxShadow": "0 2px 4px 0 rgba(0, 0, 0, 0.5), 5px 5px 10px 0 rgba(255, 255, 255, 0.2) inset, -5px -5px 10px 0 rgba(255, 255, 255, 0.2) inset"
    }}
    whileHover={{
      "backgroundColor": "rgba(255, 255, 255, 0.5)",
      transition: {
        duration: 0.2
      }
    }}
    >
    {children}
  </motion.button>;
};
export default Button;
