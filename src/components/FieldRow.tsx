import { useState } from "react"

interface FieldRowProps {
    showDelete: boolean
    id: number
    dataTypes: Array<string>
    onAddField: (id: number) => void
}

const FieldRow = (props: FieldRowProps) => {
    const [fieldName, setFieldName] = useState<string>("")
    const [fieldType, setFieldType] = useState<string>("")

    return (
        <div className="horizontal-alignment">
            <div className="horizontal-alignment">
                <p>Field name:&nbsp;</p>
                <input type="text" value={fieldName} onChange={(event) => { setFieldName(event.target.value) }} />
            </div>
            <div className="horizontal-alignment">
                <p>Field type:&nbsp;</p>
                <select name="field-type" id="field-type">
                    {
                        props.dataTypes.map((dataType) => {
                            return <option value={dataType}>{dataType}</option>
                        })
                    }
                </select>
            </div>
            <div className="horizontal-alignment">
                <button onClick={() => { props.onAddField(props.id) }}>+</button>
                <span>&nbsp;&nbsp;</span>
                {
                    props.showDelete &&
                    <button>delete</button>
                }
            </div>
        </div>
    )
}

export default FieldRow