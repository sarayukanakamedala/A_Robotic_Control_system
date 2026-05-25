import { supabase } from "./supabase"

export async function getGestures(){

const {data} = await supabase
.from("gesture_logs")
.select("*")

return data

}