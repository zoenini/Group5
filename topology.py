#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
import sys

class CustomTopo(Topo):
	"Simple Data Center Topology"

	"linkopts - (1:core, 2:aggregation, 3: edge) parameters"
	"fanout - number of child switch per parent switch"
	def __init__(self,fanout=2, **opts):
		# Initialize topology and default options
		Topo.__init__(self, **opts)

		self.fanout = fanout	
		avg_cpu = 0.5/(fanout**3)
		linkopts1 = dict(bw=50, delay='5ms', loss=0, max_queue_size=1000, use_htb=True)
		linkopts2 = dict(bw=30, delay='5ms', loss=0, max_queue_size=1000, use_htb=True)
		linkopts3 = dict(bw=20, delay='5ms', loss=0, max_queue_size=1000, use_htb=True)
		# Add hosts and switches
		core = self.addSwitch('c1')
		#for i in range(1,fanout+1):
			#aggregation = self.addSwitch('a%s' % i)
			#self.addLink(core,aggregation,**linkopts1)
			#for j in range(1,fanout+1):

		edge = self.addSwitch('s1')
		self.addLink(core,edge,**linkopts2)
		host = self.addHost('CEO', cpu=avg_cpu)
		self.addLink(edge,host,**linkopts3)
		host = self.addHost('HR_M', cpu=avg_cpu)
		self.addLink(edge,host,**linkopts3)
		host = self.addHost('Finan_M', cpu=avg_cpu)
		self.addLink(edge,host,**linkopts3)
		host = self.addHost('Tech_M', cpu=avg_cpu)
		self.addLink(edge,host,**linkopts3)
		edge = self.addSwitch('s2')
		self.addLink(core,edge,**linkopts2)
		host = self.addHost('HR_D', cpu=avg_cpu)
		self.addLink(edge,host,**linkopts3)
		host = self.addHost('Finan_D', cpu=avg_cpu)
		self.addLink(edge,host,**linkopts3)
		host = self.addHost('Tech_D', cpu=avg_cpu)
		self.addLink(edge,host,**linkopts3)
		edge = self.addSwitch('s3')
		self.addLink(core,edge,**linkopts2)
		host = self.addHost('HR_Data', cpu=avg_cpu)
		self.addLink(edge,host,**linkopts3)
		host = self.addHost('Finan_Data', cpu=avg_cpu)
		self.addLink(edge,host,**linkopts3)
		host = self.addHost('Tech_Data', cpu=avg_cpu)
		self.addLink(edge,host,**linkopts3)
				#for k in range(1,fanout+1):
		#edge = self.addSwitch('s1')
		#self.addLink(core,edge,**linkopts2)
		#host = self.addHost('CEO', cpu=avg_cpu)
		#self.addLink(edge,host,**linkopts3)
		#host = self.addHost('Financial', cpu=avg_cpu)
		#self.addLink(edge,host,**linkopts3)
		#edge = self.addSwitch('s2')
		#self.addLink(core,edge,**linkopts2)
		#host = self.addHost('h3', cpu=avg_cpu)
		#self.addLink(edge,host,**linkopts3)
		#host = self.addHost('h4', cpu=avg_cpu)
		#self.addLink(edge,host,**linkopts3)



#def perfTest(no_child):

#	"Create network and run simple performance test"

#	topo = CustomTopo(linkopts1="--link bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True",
#	linkopts2="--link bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True",
#	linkopts3="--link bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True", fanout=no_child)
#	net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
#	net.start()
#	print "Dumping host connections"
#	dumpNodeConnections(net.hosts)
#	print "Testing network connectivity"
#	net.pingAll()
#	print "Testing bandwidth between h1 and h5"
#	h1, h4 = net.get('h1', 'h4')
#	net.iperf((h1, h4))
#	print "Testing bandwidth between h1 and e1"
#	h1, e1 = net.get('h1', 'e1')
	#net.iperf((h1, e1))
#	net.stop()


#if __name__ == '__main__':
#	setLogLevel('info')
#	perfTest(int(sys.argv[1]))
#	perfTest(3)

#topos = { 'prelab2': ( lambda: prelab2Topo() ) }
topos = { 'custom': ( lambda: CustomTopo() ) }
