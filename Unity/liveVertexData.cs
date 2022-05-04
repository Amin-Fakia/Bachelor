using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using UnityEditor;
using UnityEngine.Networking;
using Newtonsoft.Json;
public class liveVertexData : MonoBehaviour
{
    // Start is called before the first frame update
    
    float[] myList;  
    Color[] colors;
    [System.Serializable]

        public class Root
    {
        public List<List<double>> mylist { get; set; }
    }
    
    // [System.Serializable]
    // public class Root
    // {
    //     public List<colorValues> mylist { get; set; }
    // }

    public List<List<double>> myColorValues;


    Root myObject;
    Root stuff;
    private string baseName;
    Mesh mesh;
    TextAsset asset;
    Vector3[] vertices;
    void Start()
    {
        //myObject = JsonUtility.FromJson<Root>(asset.text);
        
        QualitySettings.vSyncCount = 0;
        Application.targetFrameRate = 30;
        DirectoryInfo directoryInfo = new DirectoryInfo(Application.streamingAssetsPath);
        Debug.Log("Streaming Assets Path: " + Application.streamingAssetsPath);
        FileInfo[] allFiles = directoryInfo.GetFiles("*.*");
        Debug.Log(allFiles);
        this.asset = Resources.Load<TextAsset>("liveData");
        Debug.Log(this.asset);
        this.stuff = JsonConvert.DeserializeObject<Root>(asset.text);
        Debug.Log(stuff.mylist.Count);
        //Debug.Log(stuff.mylist[0]);
       

        this.mesh = this.GetComponent<MeshFilter>().mesh;
        this.vertices = mesh.vertices;
        //Debug.Log(asset.text);
        Debug.Log(this.vertices.Length);
        colors = new Color[vertices.Length];
        for (int i = 0; i < vertices.Length; i++) {
            //colors[i] = Color.black;
            colors[i] = new Color((float)stuff.mylist[i][0]/255,(float)stuff.mylist[i][1]/255,(float)stuff.mylist[i][2]/255,(float)stuff.mylist[i][3]/255);
        }
        // Debug.Log(colors);
        Debug.Log(Application.persistentDataPath);
        this.mesh.colors = colors;
        // foreach(Color c in mesh.colors) {
            
        //     // Debug.Log(c.r);
        //     // Debug.Log(c.g);
        //     // Debug.Log(c.b);
        // }
        
    }

    // Update is called once per frame
    void Update()
    {
        StartCoroutine(GetRequest());
        
        // string wwwStreamFilePath = "file://" + "liveData.json";
        // WWW www = new WWW(wwwStreamFilePath);
        // yield return www;
        // //this.asset = Resources.Load<TextAsset>("liveData");
        // this.stuff = JsonConvert.DeserializeObject<Root>(this.asset.text);
        // for (int i = 0; i < vertices.Length; i++) {
        //     //colors[i] = Color.red;
        //     colors[i] = new Color((float)this.stuff.mylist[i][0]/255,(float)this.stuff.mylist[i][1]/255,(float)this.stuff.mylist[i][2]/255,(float)this.stuff.mylist[i][3]/255);
        // }
        // this.mesh.colors = colors;
        
    }
     IEnumerator GetRequest()
    {
        string uri = "http://127.0.0.1:5000/";
        using(UnityWebRequest request = UnityWebRequest.Get(uri)){

            yield return request.SendWebRequest();
            
            if(request.isNetworkError || request.isHttpError) {
                
            } else {
                this.stuff = JsonConvert.DeserializeObject<Root>(request.downloadHandler.text);
                for (int i = 0; i < vertices.Length; i++) {
            //colors[i] = Color.red;
                    colors[i] = new Color((float)this.stuff.mylist[i][0]/255,(float)this.stuff.mylist[i][1]/255,(float)this.stuff.mylist[i][2]/255,(float)this.stuff.mylist[i][3]/255);
                }
                this.mesh.colors = colors;
                
                
            }

        };

    }
    IEnumerator getData() {
        
        //string path = File.ReadAllText(Application.streamingAssetsPath + "/liveData.json");
        //StreamReader SR = new StreamReader(Application.streamingAssetsPath + "/liveData.json");
        
         // file is automatically closed after reaching the end of the using block
        string path = File.ReadAllText(Application.streamingAssetsPath + "/liveData.json");
        yield return path;
        //this.asset = Resources.Load<TextAsset>("liveData");
        this.stuff = JsonConvert.DeserializeObject<Root>(path);
        for (int i = 0; i < vertices.Length; i++) {
            //colors[i] = Color.red;
            colors[i] = new Color((float)this.stuff.mylist[i][0]/255,(float)this.stuff.mylist[i][1]/255,(float)this.stuff.mylist[i][2]/255,(float)this.stuff.mylist[i][3]/255);
        }
        this.mesh.colors = colors;
        
    }
}
