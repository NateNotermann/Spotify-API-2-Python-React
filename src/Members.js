import React, {useState, useEffect} from 'react' 

function Members(){

  const [data, setData] = useState([{}])

  useEffect(() => {
    fetch("/members").then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log('data', data);
      }
    )
  }, [])


  return (
    <div>
        <p>This is the Members COMPONENT</p>
        {(typeof data.members === 'undefined') ?(
            <p>loading..</p>
        ): (
          data.members.map((member, i) => (
            <p key={i}>{member}</p>
          ))
        )
      }

    </div>  
  )
}

export default Members;