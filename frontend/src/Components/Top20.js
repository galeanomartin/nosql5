import React, { useState, useEffect } from 'react'
import axios from 'axios'
import Listado from './Listado'

function Top20() {

  const [listado, setListado] = useState([])
  const [loading, setLoading] = useState(false)

  const listarTop20 = () => {
    axios.get('http://localhost:5000/top20').then((res) => {
      if (res !== null) {
        console.log(res.data)
        setListado(res.data)
        setLoading(false)
      } else {
        setLoading(true)
      }
    })
      .catch((error) => {
        console.log(error);
      })
  }

  useEffect(() => {
    listarTop20();
    setLoading(true)
  }, [])

  const style = {
    width: '70%'
  }

  const styleLoader = {
    position: 'absolute',
    top: '50%',
    left: '60%',

    marginLeft: '-300px'

  }

  return (
    <div>
      <br></br>
      <h2 align="center">Top 20 de Criptomonedas</h2>
      <div align="center">
        <table className="table table-striped table-hover table-condensed mt-5" style={style}>
          <thead className="thead-dark">
            <tr>
              {/*<th scope="col" className="text text-center ">Id</th>*/}
              <th scope="col" className="text text-center ">Pos. Ranking</th>
              <th scope="col" className="text text-center">Nombre</th>
              <th scope="col" className="text text-center">Símbolo</th>
              <th scope="col" className="text text-center">Precio USD</th>
              <th scope="col" className="text text-center">Detalles</th>
            </tr>
          </thead>
          <tbody>
            {(loading) ? <div style={styleLoader} >
              <h3>Cargando datos... </h3></div> :
              listado.map(thing => (
                <Listado
                  key={thing.id}
                  thing={thing}
                />
              ))
            }

          </tbody>
        </table>

      </div>
    </div>


  )
}

export default Top20;