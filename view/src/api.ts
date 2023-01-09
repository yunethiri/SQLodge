import apisauce from 'apisauce'
import { RelationView } from './App'

const api = apisauce.create({
    baseURL: "http://localhost:2222",
})

export async function createRelation(relationData: any) {
    let res = await api.post("/table-create", relationData)
    if (res.ok) {
        alert("Created relation named " + relationData.name)
    } else {
        alert("Failed to create relation named " + relationData.name)
    }
}

export async function getRelation(relationName: string) {
    let res = await api.get("/table", { "name": relationName })
    if (res.ok) {
        return res.data as Promise<RelationView>
    } else {
        let data: RelationView = {
            columns: [],
            rows: [],
        }
        return data
    }

}

export async function insertEntry(entry: any) {
    let res = await api.post("/table-insert", entry)
    if (res.ok) {
        console.log("Inserted successfully!")
    }
}

export async function updateEntry(entry: any) {
    let res = await api.post("/table-update", entry)
    if (res.ok) {
        console.log("Inserted successfully!")
    }
}
