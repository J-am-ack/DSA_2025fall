#include <iostream>
#include <vector>
#include <unordered_map>
using namespace std;
struct node
{
	string name;
	vector<pair<node *, int>> neighbor_node;
	bool find=false;
	node (string named) : name(named) {};
};
int min_result=1<<30;
unordered_map<string, node *> umap;
vector<pair<string,int>>path;
vector<pair<string,int>>result;
void dfs(node* begin,node* end,node* last_cur,int path_result){

	if(path_result>=min_result)return;
	if(begin==end){
		if(path_result<min_result){
			min_result=path_result;
			result=path;
		}
		return;
	}
	node *next;
	for(int i=0;i<begin->neighbor_node.size();i++){
		if(begin->neighbor_node[i].first!=last_cur&&!begin->neighbor_node[i].first->find){
			next=begin->neighbor_node[i].first;
			next->find=true;
			path.push_back(make_pair(next->name,begin->neighbor_node[i].second));
			dfs(next,end,begin,path_result+begin->neighbor_node[i].second);
			next->find=false;
			path.pop_back();
		}
	}
}
int main()
{
	int P;
	cin >> P;
	
	for (int i = 0; i < P; i++)
	{
		string name;
		cin >> name;
		umap[name] = new node(name);
	}
	int Q;
	cin >> Q;
	for (int i = 0; i < Q; i++)
	{
		string a, b;
		int c;
		cin >> a >> b >> c;
		umap[a]->neighbor_node.push_back(make_pair(umap[b], c));
		umap[b]->neighbor_node.push_back(make_pair(umap[a], c));
	}
	
	int R;
	cin>>R;
	for(int i=0;i<R;i++){
		result.clear();
		path.clear();
		min_result=1<<30;
		string begin,end;
		cin>>begin>>end;
		umap[begin]->find=true;
		dfs(umap[begin],umap[end],umap[begin],0);
		umap[begin]->find=false;
		
		cout<<begin;
		
		for(int j=0;j<result.size();j++){
			cout<<"->("<<result[j].second<<")->"<<result[j].first;
		}
		cout<<endl;
	}
	
}