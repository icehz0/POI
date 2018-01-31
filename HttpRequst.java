package getdata;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import java.util.List;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
public class HttpRequst {
	//最终结果
	public static List<Integer> numbers=new ArrayList<>();
	//发送请求
	public static String sendGet(String url){
        String result = "";
        BufferedReader in = null;
        try {
            URL realUrl = new URL(url);
            // 打开和URL之间的连接
            URLConnection connection = realUrl.openConnection();
            // 建立实际的连接
            connection.connect();
            // 定义 BufferedReader输入流来读取URL的响应
            in = new BufferedReader(new InputStreamReader(
                    connection.getInputStream()));
            String line;
            while ((line = in.readLine()) != null) {
                result += line;
            }
        } catch (Exception e) {
            System.out.println("发送GET请求出现异常！" + e);
            e.printStackTrace();
        }
        // 使用finally块来关闭输入流
        finally {
            try {
                if (in != null) {
                    in.close();
                }
            } catch (Exception e2) {
                e2.printStackTrace();
            }
        }
        return result;
    }
	public static String getJson(String locname){
		
		HttpRequst httpRequst = new HttpRequst();//建立网页请求链接对象
		//设置URL网址格式
        String url = "http://api.map.baidu.com/place/v2/search?query=工厂&page_size=20&page_num=0&scope=1&coord_type=1&location=";
        StringBuilder sb = new StringBuilder();//存放网址
        sb.append(url);
        sb.append(locname);
        sb.append("&radius=1000&output=json&ak=Vn1ebvMZ1DCw2nj5LSQ738gmOB8AkCce");
        String json_result = httpRequst.sendGet(sb.toString());
		return json_result;
	}
	
	public static int parser(String json){
		JSONObject jsonParse = JSON.parseObject(json);
		int factoryNumber=jsonParse.getIntValue("total");
		
		return factoryNumber;	
	}
	public static int parserIF(String json){
		JSONObject jsonParse = JSON.parseObject(json);
		int factoryNumber=jsonParse.getIntValue("status");
		return factoryNumber;	
	}
	public static JSONArray parserfactory(String json){
		
		JSONObject jsonParse = JSON.parseObject(json);
		JSONArray noArr = jsonParse.getJSONArray("results");
		return noArr;
	}
		
	public static void main(String[] args) {
		
		//读取数据
		Readfile rf=new Readfile();
		List<String> factoryName=new ArrayList<>();
		List<GPS> gpss=new ArrayList<>();
		gpss=rf.readGps();
		List<Integer> factoryNUMBS=new ArrayList<>(); 
		int factoryNumber=0;
		HttpRequst hre=new HttpRequst();
		String locname="";
		String result="";
		for (int i = 0; i <gpss.size(); i++) {
			//经纬度
			locname=gpss.get(i).getLng()+","+gpss.get(i).getLat();
			//返回的json
			result=hre.getJson(locname);
			//判断返回状态是否正确
			if (hre.parserIF(result)==0) {
				factoryNumber=hre.parser(result);
				hre.numbers.add(factoryNumber);
				System.out.println(gpss.get(i).getLat()+","+gpss.get(i).getLng()+","+factoryNumber);
				JSONArray ja=hre.parserfactory(result);
//				System.out.println(ja);
			} else {
				System.out.println(locname);
			}
			
		}		
	}	
}
