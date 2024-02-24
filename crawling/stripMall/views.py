from django.shortcuts import render
from rest_framework.response import Response
from .models import Mall
from rest_framework.views import APIView
from .serializers import MallSerializer
import requests
from user_agent import generate_user_agent, generate_navigator
import math
# Create your views here.
class MallListAPI(APIView):
    def get(self, request):
        queryset = Mall.objects.all()
        print(queryset)
        serializer = MallSerializer(queryset, many=True)
        return Response(serializer.data)


class getMallList(APIView):
    def get(self,request):
        headers = {'User-Agent': generate_user_agent(device_type='smartphone')}
        lat = request.GET.get('lat','37.501558')
        lon = request.GET.get('lot','127.037691')

        # 최초 요청 시 디폴트 값으로 설정되어 있으나, 원하는 값으로 구성
        rletTpCds="SG" #상가
        tradTpCds="A1:B1:B2" #매매/전세/월세 매물 확인
        z = "18" #줌크기

        # 0.1 = 11km
        # 0.01 = 1km
        # 0.001 = 100m
        # 0.0001 = 10m
        # 0.00001 = 1m
        lat_margin = 0.003 #중심좌표로부터 위도 +-
        lon_margin = 0.003 #중심좌표로부터 경도 +-
        btm=float(lat)-lat_margin
        lft=float(lon)-lon_margin
        top=float(lat)+lat_margin
        rgt=float(lon)+lon_margin
        remaked_URL = "https://m.land.naver.com/cluster/clusterList?view=atcl&ortarNo=&rletTpCd={}&tradTpCd={}&z={}&lat={}&lon={}&btm={}&lft={}&top={}&rgt={}"\
        .format(rletTpCds,tradTpCds,z, lat, lon,btm,lft,top,rgt)
        res2 = requests.get(remaked_URL,headers=headers)
        json_str = res2.json()
        return Response(json_str)

class getMallDetailList(APIView):
    def get(self,request):
        lgeo = request.GET.get('lgeo')
        count = request.GET.get('count')
        z = request.GET.get('z')
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        cortarNo = request.GET.get('cortarNo')
        rletTpCds="SG" #상가
        tradTpCds="A1:B1:B2" #매매/전세/월세 매물 확인
        idx = request.GET.get('idx')
        headers = {'User-Agent': generate_user_agent(device_type='smartphone')}

        remaked_URL2 = "https://m.land.naver.com/cluster/ajax/articleList?""itemId={}&mapKey=&lgeo={}&showR0=&" \
        "rletTpCd={}&tradTpCd={}&z={}&lat={}&""lon={}&totCnt={}&cortarNo={}&page={}"\
            .format(lgeo, lgeo, rletTpCds, tradTpCds, z, lat, lon, count,cortarNo, idx)
        res3 = requests.get(remaked_URL2,headers=headers)
        # atclNo = v['atclNo']        # 물건번호
        # rletTpNm = v['rletTpNm']    # 상가구분
        # tradTpNm = v['tradTpNm']    # 매매/전세/월세 구분
        # prc = v['prc']              # 가격
        # spc1 = v['spc1']            # 계약면적(m2) -> 평으로 계산 : * 0.3025
        # spc2 = v['spc2']            # 전용면적(m2) -> 평으로 계산 : * 0.3025
        # hanPrc = v['hanPrc']        # 보증금                
        # rentPrc = v['rentPrc']      # 월세
        # flrInfo = v['flrInfo']      # 층수(물건층/전체층)
        # tagList = v['tagList']      # 기타 정보
        # rltrNm = v['rltrNm']        # 부동산
        # detaild_information = "https://m.land.naver.com/article/info/{}".format(atclNo)
        #img = https://landthumb-phinf.pstatic.net/~~
        print(remaked_URL2)
        result = res3.json()
        return Response(result)