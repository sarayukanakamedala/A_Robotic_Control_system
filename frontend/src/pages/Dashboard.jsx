import { useEffect, useState } from "react"
import { getGestures } from "../services/api"

export default function Dashboard(){

const [gestures,setGestures] = useState([])

useEffect(()=>{

async function load(){

const data = await getGestures()

setGestures(data)

}

load()

},[])

return(

<div>

<h1>Gesture Logs</h1>

{gestures.map(g=>(
<div key={g.id}>
{g.gesture}
</div>
))}

</div>

)

}