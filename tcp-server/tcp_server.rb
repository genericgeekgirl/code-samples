require 'socket'
require 'concurrent-ruby'

BUFFER_SIZE = 10

class Server
  def initialize(port)
    @server = TCPServer.new(port)
    @connections = Concurrent::Hash.new
    @buffer = []
    puts "Listening on port #{port}"
    # default is a listen queue size of 5
  end
  
  def run
    # ctrl-c
    trap("INT") do
      puts("\nShutting down!")
      broadcast(nil, "Shutting down the server!")
      @server.close
      exit
    end
    
    Socket.accept_loop(@server) do | client |
      Thread.new do
        client.puts("What is your nickname?")
        while username = client.gets.strip
          break unless username.empty? || @connections.has_key?(username)
          client.puts("Try another name.")
        end

        count = @connections.count
        connection_string = "You are connected with #{count} user(s)"
        connection_string += count == 0 ? "." : ": #{@connections.keys.join(',')}"        
        client.puts(connection_string)

        @buffer.each do | line |
          client.puts(line)
        end
        
        @connections[username] = client
        broadcast(client, "#{username} has entered the chat")

        while message = client.gets do
          broadcast(client, "<#{username}> #{message}") unless message.chomp.empty?
        end

        client.close
        @connections.delete(@connections.key(client))
        broadcast(client, "#{username} has left the chat.")
      end
    end
  end

  private def broadcast(sender, message)
    timestamp = Time.now.strftime("%H:%M:%S")
    line = "#{timestamp} #{message}"

    @connections.values.each do | recipient |
      recipient.puts(message) if recipient != sender
    end

    @buffer << line
    @buffer.shift if @buffer.size > BUFFER_SIZE
  end
end

server = Server.new(4242)
server.run
