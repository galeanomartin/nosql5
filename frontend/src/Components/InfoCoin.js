import React, { useState, useEffect } from 'react'
import axios from 'axios'
import Swal from 'sweetalert2'


function InfoCoin({id, rank, precio}) {

  const [listado, setListado] = useState([])
  const [loading, setLoading] = useState(false)

  var number = id   
  var ranking = rank

  const buscarPorId = () => {
    axios.post('http://localhost:5000/obtenerSegunId', {
      'id': number,
    })
      .then((res) => {
        if (res !== null) {
          setListado(res.data)
          setLoading(false)
        } else {
          setLoading(true)
        }
      })
      .catch(function (error) {
        console.log(error);
      });

  }

  const borrarCrypto = async () => {
    return axios
      .post("http://localhost:5000/borrarCrypto", {
        'rank': ranking

      })
      .then(res => {
        console.log(res.data)
        Swal.fire({
          title: 'Criptomoneda eliminada!',
                      
        }).then((result) => {
          if (result.value) {
            let link = '/'
            window.location.href = link
          }
        })
      })
      .catch(err => { throw err.response.data })
  }


  const style = {
    width: '70%'
  }

  const styleLoader = {
    position: 'absolute',
    top: '50%',
    left: '60%',

    marginLeft: '-300px'


  }

  useEffect(() => {
    buscarPorId();
    setLoading(true)
  }, [])

  return (
    <div>
      {(loading) ? <div style={styleLoader} >
        <h3>Cargando datos... </h3></div> :
        <div align="center">
          < br/>
          <h2> Información de la criptomoneda</h2>
          <h2>{listado.name} ({listado.symbol})</h2>

          <table className="table table-striped table-hover table-condensed mt-5" style={style}>
            <thead className="thead-dark">
              <tr>
                {/*<th scope="col" className="text text-center ">Id</th>*/}
                <th scope="col" className="text text-center ">Pos. Ranking</th>
                <th scope="col" className="text text-center">Nombre</th>
                <th scope="col" className="text text-center">Símbolo</th>
                <th scope="col" className="text text-center">Precio USD</th>
                <th scope="col" className="text text-center">Máximo Circulante</th>
                <th scope="col" className="text text-center">Total Circulante</th>
                <th scope="col" className="text text-center"></th>
              </tr>
            </thead>

            <tbody>
              <tr className="font-weight-bold  text-black-50">
                {/*<td className="text-lg-center">{listado.id}</td>*/}
                <td className="text-lg-center">{listado.cmc_rank}</td>
                <td className="text-lg-center">{listado.name}</td>
                <td className="text-lg-center">{listado.symbol}</td>
                <td className="text-lg-center">{precio}</td>
                <td className="text-lg-center">{listado.max_supply}</td>
                <td className="text-lg-center">{listado.total_supply}</td>


                <td><button type="button" className="btn btn-danger" onClick={() => borrarCrypto()} >Eliminar Criptomoneda</button></td>
              </tr>
            </tbody>

          </table>

        </div>
      }

    </div>

  )
}
export default InfoCoin;